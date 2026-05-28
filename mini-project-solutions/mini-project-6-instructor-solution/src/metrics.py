from collections import Counter
from statistics import mean, pstdev

from src.text_utils import cosine_from_counters, lcs_length, tokenize


def bleu_like(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0
    ref_counts = Counter(ref_tokens)
    cand_counts = Counter(cand_tokens)
    overlap = sum(min(count, ref_counts[token]) for token, count in cand_counts.items())
    precision = overlap / len(cand_tokens)
    brevity = min(1.0, len(cand_tokens) / len(ref_tokens))
    return round(precision * brevity, 4)


def rouge_l(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0
    lcs = lcs_length(ref_tokens, cand_tokens)
    recall = lcs / len(ref_tokens)
    precision = lcs / len(cand_tokens)
    if recall + precision == 0:
        return 0.0
    return round((2 * recall * precision) / (recall + precision), 4)


def meteor_like(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0
    ref_counts = Counter(ref_tokens)
    cand_counts = Counter(cand_tokens)
    overlap = sum(min(count, ref_counts[token]) for token, count in cand_counts.items())
    precision = overlap / len(cand_tokens)
    recall = overlap / len(ref_tokens)
    if precision + recall == 0:
        return 0.0
    return round((10 * precision * recall) / (recall + 9 * precision), 4)


def embedding_similarity_like(reference: str, candidate: str) -> float:
    return round(cosine_from_counters(Counter(tokenize(reference)), Counter(tokenize(candidate))), 4)


def summarize(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return round(values[0], 4), 0.0
    return round(mean(values), 4), round(pstdev(values), 4)

