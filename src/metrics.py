from src.text_utils import tokenize


def bleu_like(reference: str, candidate: str) -> float:
    # TODO(STAGE 2): Implement unigram precision with brevity penalty.
    _ = tokenize(reference)
    _ = tokenize(candidate)
    return 0.0


def rouge_l(reference: str, candidate: str) -> float:
    # TODO(STAGE 2): Implement ROUGE-L using longest common subsequence.
    _ = reference
    _ = candidate
    return 0.0


def meteor_like(reference: str, candidate: str) -> float:
    # TODO(STAGE 2): Implement simple F-score style METEOR approximation.
    _ = reference
    _ = candidate
    return 0.0


def embedding_similarity_like(reference: str, candidate: str) -> float:
    # TODO(STAGE 2): Use lexical cosine or real embedding cosine.
    _ = reference
    _ = candidate
    return 0.0

