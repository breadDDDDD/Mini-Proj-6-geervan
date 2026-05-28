import csv
import json
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
    # TODO(STAGE 1): Use pypdf.PdfReader to extract text.
    return ""


def read_csv(path: Path) -> str:
    # TODO(STAGE 1): Read CSV rows and convert each row into searchable text.
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return "\n".join(str(row) for row in reader)


def read_json(path: Path) -> str:
    # This helper is provided; you may improve formatting if useful.
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)


def read_document(path: Path) -> str:
    # TODO(STAGE 1): Route by suffix: pdf, csv, json, txt/md.
    if path.suffix.lower() == ".csv":
        return read_csv(path)
    if path.suffix.lower() == ".json":
        return read_json(path)
    return ""


class LocalRetriever:
    def __init__(self, data_dir: Path | None = None, index_path: Path | None = None):
        self.data_dir = data_dir or settings.data_path
        self.index_path = index_path or settings.vector_path
        self.chunks: list[Chunk] = []

    def build(self) -> None:
        # TODO(STAGE 1): Load all local docs except gold_questions.csv, chunk, tokenize, and store chunks.
        self.chunks = []

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
        if not self.load():
            self.build()
            self.save()

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        self.ensure_loaded()
        query_tokens = tokenize(query)
        _ = query_tokens
        # TODO(STAGE 1): Score chunks and return top_k RetrievedChunk objects.
        return []


def build_index() -> None:
    retriever = LocalRetriever()
    retriever.build()
    retriever.save()


if __name__ == "__main__":
    build_index()
    print(f"Index written to {settings.vector_path}")

