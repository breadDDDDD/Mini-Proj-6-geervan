import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from src.config import settings
from src.text_utils import chunk_text, cosine_from_counters, normalize_text, tokenize


@dataclass
class Chunk:
    chunk_id: str
    filename: str
    text: str
    tokens: list[str]
    tfidf: dict[str, float]


@dataclass
class RetrievedChunk:
    chunk_id: str
    filename: str
    text: str
    score: float


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def read_csv(path: Path) -> str:
    lines = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            lines.append(" | ".join(f"{key}: {value}" for key, value in row.items()))
    return "\n".join(lines)


def read_json(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return "\n".join(json.dumps(item, ensure_ascii=False) for item in data)
    return json.dumps(data, ensure_ascii=False, indent=2)


def read_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return read_pdf(path)
    if suffix == ".csv":
        return read_csv(path)
    if suffix == ".json":
        return read_json(path)
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    return ""


def iter_documents(data_dir: Path) -> Iterable[Path]:
    for suffix in ("*.pdf", "*.txt", "*.md", "*.csv", "*.json"):
        yield from sorted(data_dir.glob(suffix))


class LocalTfidfRetriever:
    def __init__(self, data_dir: Path | None = None, index_path: Path | None = None):
        self.data_dir = data_dir or settings.data_path
        self.index_path = index_path or settings.vector_path
        self.chunks: list[Chunk] = []
        self.idf: dict[str, float] = {}

    def build(self) -> None:
        raw_chunks: list[tuple[str, str, list[str]]] = []
        for doc_path in iter_documents(self.data_dir):
            if doc_path.name == "gold_questions.csv":
                continue
            text = read_document(doc_path)
            for idx, chunk in enumerate(chunk_text(text)):
                chunk_id = f"{doc_path.name}:{idx + 1}"
                tokens = tokenize(chunk)
                raw_chunks.append((chunk_id, doc_path.name, tokens))

        doc_frequency: defaultdict[str, int] = defaultdict(int)
        for _, _, tokens in raw_chunks:
            for token in set(tokens):
                doc_frequency[token] += 1

        total_docs = max(1, len(raw_chunks))
        self.idf = {
            token: math.log((1 + total_docs) / (1 + freq)) + 1.0
            for token, freq in doc_frequency.items()
        }

        self.chunks = []
        for chunk_id, filename, tokens in raw_chunks:
            doc_text = self._find_chunk_text(chunk_id)
            self.chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    filename=filename,
                    text=doc_text,
                    tokens=tokens,
                    tfidf=self._tfidf(tokens),
                )
            )

    def _find_chunk_text(self, chunk_id: str) -> str:
        filename, idx_raw = chunk_id.rsplit(":", 1)
        idx = int(idx_raw) - 1
        text = read_document(self.data_dir / filename)
        chunks = chunk_text(text)
        return chunks[idx] if idx < len(chunks) else ""

    def _tfidf(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        if not counts:
            return {}
        max_count = max(counts.values())
        return {
            token: (count / max_count) * self.idf.get(token, 1.0)
            for token, count in counts.items()
        }

    def save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "idf": self.idf,
            "chunks": [asdict(chunk) for chunk in self.chunks],
        }
        self.index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> bool:
        if not self.index_path.exists():
            return False
        payload = json.loads(self.index_path.read_text(encoding="utf-8"))
        self.idf = {str(k): float(v) for k, v in payload.get("idf", {}).items()}
        self.chunks = [
            Chunk(
                chunk_id=item["chunk_id"],
                filename=item["filename"],
                text=item["text"],
                tokens=list(item["tokens"]),
                tfidf={str(k): float(v) for k, v in item["tfidf"].items()},
            )
            for item in payload.get("chunks", [])
        ]
        return True

    def ensure_loaded(self) -> None:
        if not self.load():
            self.build()
            self.save()

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        self.ensure_loaded()
        query_vector = Counter(self._tfidf(tokenize(normalize_text(query))))
        results = []
        for chunk in self.chunks:
            score = cosine_from_counters(query_vector, Counter(chunk.tfidf))
            if score > 0:
                results.append(
                    RetrievedChunk(
                        chunk_id=chunk.chunk_id,
                        filename=chunk.filename,
                        text=chunk.text,
                        score=round(score, 4),
                    )
                )
        results.sort(key=lambda item: item.score, reverse=True)
        return results[: top_k or settings.top_k]


def build_index() -> None:
    retriever = LocalTfidfRetriever()
    retriever.build()
    retriever.save()


if __name__ == "__main__":
    build_index()
    print(f"Index written to {settings.vector_path}")

