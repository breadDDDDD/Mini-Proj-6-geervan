import math
from collections import Counter

from src.text_utils import tokenize


def _safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def bleu_like(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not cand_tokens:
        return 0.0

    ref_counts = Counter(ref_tokens)
    cand_counts = Counter(cand_tokens)
    overlap = sum(min(count, ref_counts[token]) for token, count in cand_counts.items())
    precision = _safe_div(overlap, len(cand_tokens))

    if len(cand_tokens) > len(ref_tokens):
        brevity_penalty = 1.0
    else:
        brevity_penalty = math.exp(1 - _safe_div(len(ref_tokens), len(cand_tokens)))

    return round(precision * brevity_penalty, 6)


def _lcs_length(a: list[str], b: list[str]) -> int:
    if not a or not b:
        return 0
    dp = [0] * (len(b) + 1)
    for token_a in a:
        prev = 0
        for j, token_b in enumerate(b, start=1):
            current = dp[j]
            if token_a == token_b:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = current
    return dp[-1]


def rouge_l(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0

    lcs = _lcs_length(ref_tokens, cand_tokens)
    recall = _safe_div(lcs, len(ref_tokens))
    precision = _safe_div(lcs, len(cand_tokens))
    if recall == 0.0 and precision == 0.0:
        return 0.0

    beta = 1.2
    score = ((1 + beta**2) * precision * recall) / (recall + (beta**2) * precision)
    return round(score, 6)


def meteor_like(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0

    ref_counts = Counter(ref_tokens)
    cand_counts = Counter(cand_tokens)
    matches = sum(min(count, ref_counts[token]) for token, count in cand_counts.items())

    precision = _safe_div(matches, len(cand_tokens))
    recall = _safe_div(matches, len(ref_tokens))
    if precision == 0.0 and recall == 0.0:
        return 0.0

    alpha = 0.9
    score = (precision * recall) / ((1 - alpha) * recall + alpha * precision)
    return round(score, 6)


def embedding_similarity_like(reference: str, candidate: str) -> float:
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0

    ref_counts = Counter(ref_tokens)
    cand_counts = Counter(cand_tokens)
    common = set(ref_counts) & set(cand_counts)
    dot = sum(ref_counts[token] * cand_counts[token] for token in common)
    ref_norm = math.sqrt(sum(value * value for value in ref_counts.values()))
    cand_norm = math.sqrt(sum(value * value for value in cand_counts.values()))
    if ref_norm == 0 or cand_norm == 0:
        return 0.0

    return round(dot / (ref_norm * cand_norm), 6)
