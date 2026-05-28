import math
import re
from collections import Counter


TOKEN_RE = re.compile(r"[A-Za-z0-9]+", re.UNICODE)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def cosine_from_counters(a: Counter, b: Counter) -> float:
    # TODO(STAGE 1): Implement cosine similarity for sparse lexical vectors.
    return 0.0


def chunk_text(text: str, chunk_size: int = 850, overlap: int = 120) -> list[str]:
    # TODO(STAGE 1): Split long documents into overlapping chunks.
    text = normalize_text(text)
    return [text] if text else []

