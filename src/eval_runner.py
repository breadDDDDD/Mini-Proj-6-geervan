import argparse
import csv
import time
from pathlib import Path

from src.config import settings
from src.costing import estimate_cost_idr
from src.generator import build_context, get_generator
from src.metrics import bleu_like, embedding_similarity_like, rouge_l
from src.retriever import LocalRetriever
from src.safety import check_safety
from src.text_utils import estimate_tokens, tokenize


REPORTS_DIR = Path("reports")


def _grounded_score(answer: str, context: str) -> float:
    answer_tokens = tokenize(answer)
    if not answer_tokens:
        return 0.0
    context_terms = set(tokenize(context))
    if not context_terms:
        return 0.0
    supported = sum(1 for token in answer_tokens if token in context_terms)
    return supported / len(answer_tokens)


def run_eval(variant: str, top_k: int | None = None) -> Path:
    retriever = LocalRetriever()
    generator = get_generator()
    effective_top_k = top_k if top_k is not None else settings.top_k

    gold_path = settings.data_path / "gold_questions.csv"
    with gold_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / f"eval_report_{variant}.csv"

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "question_id",
                "variant",
                "status",
                "bleu",
                "rouge_l",
                "embedding_similarity",
                "retrieval_hit",
                "grounded",
                "refusal",
                "latency_ms",
                "cost_idr",
            ],
        )
        writer.writeheader()

        for row in rows:
            query = row["query"]
            expected_answer = row["expected_answer"]
            expected_source = row["expected_source"]
            expected_refusal = row["expected_refusal"].strip().lower() == "true"

            started = time.perf_counter()
            safety = check_safety(query)

            if not safety["allowed"]:
                answer = ""
                chunks = []
                status = "refused"
                refusal = True
            else:
                chunks = retriever.search(query, top_k=effective_top_k)
                answer = generator.generate(query, chunks)
                status = "ok"
                refusal = False

            latency_ms = int((time.perf_counter() - started) * 1000)
            context = build_context(chunks)
            input_tokens = estimate_tokens(query + "\n" + context)
            output_tokens = estimate_tokens(answer)
            sources = [chunk.filename for chunk in chunks]

            retrieval_hit = expected_source in sources if expected_source else True
            grounded = _grounded_score(answer, context) >= 0.5
            refusal_correct = refusal == expected_refusal

            writer.writerow(
                {
                    "question_id": row["question_id"],
                    "variant": variant,
                    "status": status,
                    "bleu": bleu_like(expected_answer, answer),
                    "rouge_l": rouge_l(expected_answer, answer),
                    "embedding_similarity": embedding_similarity_like(expected_answer, answer),
                    "retrieval_hit": int(retrieval_hit),
                    "grounded": int(grounded),
                    "refusal": int(refusal_correct),
                    "latency_ms": latency_ms,
                    "cost_idr": estimate_cost_idr(input_tokens, output_tokens),
                }
            )

    print(f"Wrote eval report to {output_path} (variant={variant}, top_k={effective_top_k})")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", default="A")
    parser.add_argument("--top-k", type=int, default=None)
    args = parser.parse_args()
    _ = settings
    run_eval(args.variant, args.top_k)


if __name__ == "__main__":
    main()
