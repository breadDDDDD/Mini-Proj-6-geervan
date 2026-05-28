import argparse
import csv
import os
import time
from pathlib import Path

from src.config import settings
from src.costing import estimate_cost_idr
from src.generator import build_context, get_generator
from src.metrics import bleu_like, embedding_similarity_like, meteor_like, rouge_l
from src.retriever import LocalTfidfRetriever
from src.safety import check_safety
from src.text_utils import estimate_tokens


REPORTS_DIR = Path("reports")


def expected_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def run_eval(variant: str, top_k: int | None = None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    gold_path = settings.data_path / "gold_questions.csv"
    retriever = LocalTfidfRetriever()
    generator = get_generator()
    rows = []

    with gold_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for item in reader:
            query = item["query"]
            expected_answer = item["expected_answer"]
            expected_source = item["expected_source"]
            expected_refusal = expected_bool(item.get("expected_refusal", "false"))

            started = time.perf_counter()
            safety = check_safety(query)
            if not safety["allowed"]:
                answer = "REFUSED"
                chunks = []
                refusal = True
            else:
                chunks = retriever.search(query, top_k=top_k or settings.top_k)
                answer = generator.generate(query, chunks)
                refusal = False
            latency_ms = int((time.perf_counter() - started) * 1000)

            source_names = [chunk.filename for chunk in chunks]
            retrieval_hit = expected_source in source_names if expected_source else refusal == expected_refusal
            grounded = refusal or retrieval_hit
            context = build_context(chunks)
            input_tokens = estimate_tokens(query + "\n" + context)
            output_tokens = estimate_tokens(answer)

            rows.append(
                {
                    "question_id": item["question_id"],
                    "variant": variant,
                    "query_type": item.get("query_type", "normal"),
                    "status": "refused" if refusal else "ok",
                    "expected_refusal": expected_refusal,
                    "refusal": refusal,
                    "refusal_correct": refusal == expected_refusal,
                    "expected_source": expected_source,
                    "sources": "|".join(source_names),
                    "retrieval_hit": retrieval_hit,
                    "grounded": grounded,
                    "bleu": bleu_like(expected_answer, answer) if not refusal else 0.0,
                    "rouge_l": rouge_l(expected_answer, answer) if not refusal else 0.0,
                    "meteor": meteor_like(expected_answer, answer) if not refusal else 0.0,
                    "embedding_similarity": embedding_similarity_like(expected_answer, answer) if not refusal else 0.0,
                    "latency_ms": latency_ms,
                    "input_tokens_est": input_tokens,
                    "output_tokens_est": output_tokens,
                    "cost_idr": estimate_cost_idr(input_tokens, output_tokens),
                }
            )

    output_path = REPORTS_DIR / f"eval_report_{variant}.csv"
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", default=os.getenv("VARIANT", "A"))
    parser.add_argument("--top-k", type=int, default=None)
    args = parser.parse_args()
    run_eval(args.variant, args.top_k)


if __name__ == "__main__":
    main()

