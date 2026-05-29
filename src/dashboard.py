import csv
import statistics
from pathlib import Path

import matplotlib.pyplot as plt


REPORTS_DIR = Path("reports")


def _read_report(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _mean(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    index = max(0, min(len(sorted_vals) - 1, int(0.95 * (len(sorted_vals) - 1))))
    return sorted_vals[index]


def _summarize(rows: list[dict[str, str]]) -> dict[str, float]:
    latencies = [float(row["latency_ms"]) for row in rows]
    costs = [float(row["cost_idr"]) for row in rows]
    refusal_acc = [float(row["refusal"]) for row in rows]
    grounded = [float(row["grounded"]) for row in rows]
    retrieval_hit = [float(row["retrieval_hit"]) for row in rows]
    bleu = [float(row["bleu"]) for row in rows]
    rouge = [float(row["rouge_l"]) for row in rows]
    embedding = [float(row["embedding_similarity"]) for row in rows]

    return {
        "samples": float(len(rows)),
        "latency_p50_ms": statistics.median(latencies) if latencies else 0.0,
        "latency_p95_ms": _p95(latencies),
        "avg_cost_idr": _mean(costs),
        "refusal_accuracy": _mean(refusal_acc),
        "groundedness_rate": _mean(grounded),
        "retrieval_hit_rate": _mean(retrieval_hit),
        "bleu_mean": _mean(bleu),
        "rouge_l_mean": _mean(rouge),
        "embedding_similarity_mean": _mean(embedding),
    }


def _write_ab_comparison(summary_a: dict[str, float], summary_b: dict[str, float], output_path: Path) -> None:
    fieldnames = [
        "metric",
        "variant_a",
        "variant_b",
        "delta_b_minus_a",
    ]
    metric_rows = [
        "samples",
        "latency_p50_ms",
        "latency_p95_ms",
        "avg_cost_idr",
        "refusal_accuracy",
        "groundedness_rate",
        "retrieval_hit_rate",
        "bleu_mean",
        "rouge_l_mean",
        "embedding_similarity_mean",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for metric in metric_rows:
            a_val = summary_a.get(metric, 0.0)
            b_val = summary_b.get(metric, 0.0)
            writer.writerow(
                {
                    "metric": metric,
                    "variant_a": round(a_val, 6),
                    "variant_b": round(b_val, 6),
                    "delta_b_minus_a": round(b_val - a_val, 6),
                }
            )


def _render_dashboard(summary_a: dict[str, float], summary_b: dict[str, float], output_path: Path) -> None:
    labels = ["P95 Latency (ms)", "Cost / Query (IDR)", "Refusal Accuracy", "Groundedness"]
    a_vals = [
        summary_a["latency_p95_ms"],
        summary_a["avg_cost_idr"],
        summary_a["refusal_accuracy"],
        summary_a["groundedness_rate"],
    ]
    b_vals = [
        summary_b["latency_p95_ms"],
        summary_b["avg_cost_idr"],
        summary_b["refusal_accuracy"],
        summary_b["groundedness_rate"],
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    axes = axes.flatten()

    for idx, axis in enumerate(axes):
        axis.bar(["A", "B"], [a_vals[idx], b_vals[idx]], color=["#1f77b4", "#ff7f0e"])
        axis.set_title(labels[idx])
        axis.grid(axis="y", alpha=0.3)

    fig.suptitle("RAG Monitoring Dashboard", fontsize=14)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report_a_path = REPORTS_DIR / "eval_report_A.csv"
    report_b_path = REPORTS_DIR / "eval_report_B.csv"
    if not report_a_path.exists() or not report_b_path.exists():
        raise FileNotFoundError("Run eval for variant A and B first.")

    rows_a = _read_report(report_a_path)
    rows_b = _read_report(report_b_path)
    summary_a = _summarize(rows_a)
    summary_b = _summarize(rows_b)

    ab_output = REPORTS_DIR / "ab_comparison.csv"
    _write_ab_comparison(summary_a, summary_b, ab_output)

    dashboard_output = REPORTS_DIR / "dashboard.png"
    _render_dashboard(summary_a, summary_b, dashboard_output)

    print(f"Wrote {ab_output}")
    print(f"Wrote {dashboard_output}")


if __name__ == "__main__":
    main()
