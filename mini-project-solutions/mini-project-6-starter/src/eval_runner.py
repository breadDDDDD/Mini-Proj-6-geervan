import argparse
import csv
from pathlib import Path

from src.config import settings


REPORTS_DIR = Path("reports")


def run_eval(variant: str, top_k: int | None = None) -> Path:
    # TODO(STAGE 2): Read data/gold_questions.csv.
    # TODO(STAGE 2): Call the same safety + retrieval + generator pipeline used by /chat.
    # TODO(STAGE 2): Compute quality, retrieval, groundedness, latency, and cost metrics.
    # TODO(STAGE 3): Respect variant and top_k so A/B compares one changed variable.
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

    print(f"Wrote placeholder report to {output_path}")
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

