import csv
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from src.config import settings
from src.text_utils import chunk_text, tokenize


@dataclass
class Chunk:
    chunk_id: str
    filename: str
    text: str
    tokens: list[str]


@dataclass
class RetrievedChunk:
    chunk_id: str
    filename: str
    text: str
    score: float


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError:
        return ""

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(page for page in pages if page.strip())


def read_csv(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[str] = []
        for row in reader:
            pieces = [f"{key}: {value}" for key, value in row.items() if value not in (None, "")]
            if pieces:
                rows.append(" | ".join(pieces))
        return "\n".join(rows)


def read_json(path: Path) -> str:
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)


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


def _cosine_from_token_lists(a: list[str], b: list[str]) -> float:
    a_counter = Counter(a)
    b_counter = Counter(b)
    dot = sum(a_counter[token] * b_counter[token] for token in set(a_counter) & set(b_counter))
    norm_a = math.sqrt(sum(value * value for value in a_counter.values()))
    norm_b = math.sqrt(sum(value * value for value in b_counter.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class LocalRetriever:
    def __init__(self, data_dir: Path | None = None, index_path: Path | None = None):
        self.data_dir = data_dir or settings.data_path
        self.index_path = index_path or settings.vector_path
        self.chunks: list[Chunk] = []

    def build(self) -> None:
        self.chunks = []
        documents = sorted(path for path in self.data_dir.rglob("*") if path.is_file())

        for path in documents:
            if path.name.lower() == "gold_questions.csv":
                continue

            text = read_document(path)
            if not text.strip():
                continue

            for index, piece in enumerate(chunk_text(text), start=1):
                tokens = tokenize(piece)
                if not tokens:
                    continue
                self.chunks.append(
                    Chunk(
                        chunk_id=f"{path.stem}_{index:03d}",
                        filename=path.name,
                        text=piece,
                        tokens=tokens,
                    )
                )

    def save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"chunks": [asdict(chunk) for chunk in self.chunks]}
        self.index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> bool:
        if not self.index_path.exists():
            return False
        payload = json.loads(self.index_path.read_text(encoding="utf-8"))
        self.chunks = [Chunk(**item) for item in payload.get("chunks", [])]
        return True

    def ensure_loaded(self) -> None:
        loaded = self.load()
        if (not loaded) or (not self.chunks):
            self.build()
            self.save()

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        self.ensure_loaded()
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        limit = top_k or settings.top_k
        scored = [
            RetrievedChunk(
                chunk_id=chunk.chunk_id,
                filename=chunk.filename,
                text=chunk.text,
                score=_cosine_from_token_lists(query_tokens, chunk.tokens),
            )
            for chunk in self.chunks
        ]
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:limit]


def build_index() -> None:
    retriever = LocalRetriever()
    retriever.build()
    retriever.save()


if __name__ == "__main__":
    build_index()
    print(f"Index written to {settings.vector_path}")
