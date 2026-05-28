import csv
from pathlib import Path
from statistics import mean, pstdev

from src.config import settings


REPORTS_DIR = Path("reports")


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(rows: list[dict], key: str) -> float:
    if not rows:
        return 0.0
    return round(sum(str(row[key]).lower() == "true" for row in rows) / len(rows) * 100, 2)


def numeric(rows: list[dict], key: str) -> list[float]:
    values = []
    for row in rows:
        try:
            values.append(float(row[key]))
        except (TypeError, ValueError):
            pass
    return values


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    idx = min(len(sorted_values) - 1, round((len(sorted_values) - 1) * p))
    return round(sorted_values[idx], 2)


def summarize_variant(path: Path) -> dict:
    rows = read_rows(path)
    normal_rows = [row for row in rows if row.get("query_type") != "adversarial"]
    bleu_values = numeric(normal_rows, "bleu")
    rouge_values = numeric(normal_rows, "rouge_l")
    similarity_values = numeric(normal_rows, "embedding_similarity")
    return {
        "variant": path.stem.replace("eval_report_", ""),
        "total": len(rows),
        "mean_bleu": round(mean(bleu_values or [0]), 4),
        "std_bleu": round(pstdev(bleu_values), 4) if len(bleu_values) > 1 else 0.0,
        "mean_rouge_l": round(mean(rouge_values or [0]), 4),
        "std_rouge_l": round(pstdev(rouge_values), 4) if len(rouge_values) > 1 else 0.0,
        "mean_similarity": round(mean(similarity_values or [0]), 4),
        "std_similarity": round(pstdev(similarity_values), 4) if len(similarity_values) > 1 else 0.0,
        "retrieval_hit_rate": pct(normal_rows, "retrieval_hit"),
        "groundedness_rate": pct(rows, "grounded"),
        "refusal_accuracy": pct(rows, "refusal_correct"),
        "p50_latency_ms": percentile(numeric(rows, "latency_ms"), 0.50),
        "p95_latency_ms": percentile(numeric(rows, "latency_ms"), 0.95),
        "mean_cost_idr": round(mean(numeric(rows, "cost_idr") or [0]), 4),
    }


def write_ab_comparison(summaries: list[dict]) -> None:
    if not summaries:
        return
    path = REPORTS_DIR / "ab_comparison.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0].keys()))
        writer.writeheader()
        writer.writerows(summaries)


def write_markdown_reports(summary: dict) -> None:
    eval_md = REPORTS_DIR / "eval_report.md"
    cost_md = REPORTS_DIR / "cost_analysis.md"
    dashboard_md = REPORTS_DIR / "dashboard.md"

    eval_md.write_text(
        f"""# Evaluation Report

## Summary

- Total questions: {summary['total']}
- Mean BLEU: {summary['mean_bleu']}
- Mean ROUGE-L: {summary['mean_rouge_l']}
- Mean embedding similarity: {summary['mean_similarity']}
- Retrieval hit-rate: {summary['retrieval_hit_rate']}%
- Groundedness rate: {summary['groundedness_rate']}%
- Refusal accuracy: {summary['refusal_accuracy']}%
- p50 latency: {summary['p50_latency_ms']} ms
- p95 latency: {summary['p95_latency_ms']} ms
- Mean cost/query: IDR {summary['mean_cost_idr']}

## Method

The evaluator runs all gold questions against the same RAG pipeline, computes lexical quality metrics,
checks expected source retrieval, verifies groundedness, and records estimated cost and latency.
""",
        encoding="utf-8",
    )

    daily_cost = summary["mean_cost_idr"] * 10_000
    monthly_cost = daily_cost * 30
    cost_md.write_text(
        f"""# Cost Analysis

## Result

- Mean cost/query: IDR {summary['mean_cost_idr']}
- Daily cost at 10k queries: IDR {daily_cost:,.0f}
- Monthly cost at 10k/day: IDR {monthly_cost:,.0f}
- Target: <= IDR 250/query
- Status: {'PASS' if summary['mean_cost_idr'] <= 250 else 'FAIL'}

## Formula

Input and output token estimates are multiplied by the configured model prices:

```text
input_tokens / 1,000,000 * INPUT_USD_PER_1M_TOKENS * IDR_PER_USD
output_tokens / 1,000,000 * OUTPUT_USD_PER_1M_TOKENS * IDR_PER_USD
```

Local retrieval and rule-based safety do not add per-query model cost.
""",
        encoding="utf-8",
    )

    dashboard_md.write_text(
        f"""# Dashboard

| Metric | Value |
|---|---:|
| Total questions | {summary['total']} |
| Retrieval hit-rate | {summary['retrieval_hit_rate']}% |
| Groundedness rate | {summary['groundedness_rate']}% |
| Refusal accuracy | {summary['refusal_accuracy']}% |
| p50 latency | {summary['p50_latency_ms']} ms |
| p95 latency | {summary['p95_latency_ms']} ms |
| Mean cost/query | IDR {summary['mean_cost_idr']} |
""",
        encoding="utf-8",
    )


def write_visual_dashboard(summary: dict) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    labels = ["Retrieval", "Grounded", "Refusal"]
    values = [
        summary["retrieval_hit_rate"],
        summary["groundedness_rate"],
        summary["refusal_accuracy"],
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values, color=["#176B87", "#64CCC5", "#DAFFFB"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Rate (%)")
    ax.set_title("LLM Monitoring Dashboard")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 1, f"{value:.1f}%", ha="center")
    ax.text(
        0.02,
        -0.18,
        f"p95 latency: {summary['p95_latency_ms']} ms | mean cost/query: IDR {summary['mean_cost_idr']}",
        transform=ax.transAxes,
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "dashboard.png", dpi=160)
    plt.close(fig)


def write_architecture_png() -> None:
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch, Rectangle
    except ImportError:
        return

    boxes = [
        ("User\nID/EN", 0.05, 0.62),
        ("FastAPI\n/chat", 0.22, 0.62),
        ("Safety\nFilter", 0.39, 0.62),
        ("Retriever\nTF-IDF", 0.56, 0.62),
        ("Generator\nFake/API", 0.73, 0.62),
        ("Answer\n+ Sources", 0.90, 0.62),
        ("Local Docs\nPDF/CSV/JSON", 0.39, 0.24),
        ("JSONL Logs", 0.64, 0.24),
        ("Eval +\nDashboard", 0.82, 0.24),
    ]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for label, x, y in boxes:
        rect = Rectangle((x - 0.06, y - 0.08), 0.12, 0.16, linewidth=1.5, edgecolor="#176B87", facecolor="#F7FBFC")
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=9)

    arrows = [
        ((0.11, 0.62), (0.16, 0.62)),
        ((0.28, 0.62), (0.33, 0.62)),
        ((0.45, 0.62), (0.50, 0.62)),
        ((0.62, 0.62), (0.67, 0.62)),
        ((0.79, 0.62), (0.84, 0.62)),
        ((0.39, 0.32), (0.54, 0.56)),
        ((0.90, 0.54), (0.66, 0.32)),
        ((0.70, 0.24), (0.76, 0.24)),
    ]
    for start, end in arrows:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=12, linewidth=1.2, color="#333333"))

    ax.text(0.5, 0.92, "Mini Project 6 Azure-Free RAG Monitoring Architecture", ha="center", fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "architecture.png", dpi=160)
    plt.close(fig)


def write_pdf_reports() -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        return

    for md_name, pdf_name in [
        ("eval_report.md", "eval_report.pdf"),
        ("cost_analysis.md", "cost_analysis.pdf"),
    ]:
        text = (REPORTS_DIR / md_name).read_text(encoding="utf-8").splitlines()
        pdf_path = REPORTS_DIR / pdf_name
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height = A4
        y = height - 45
        c.setFont("Helvetica", 10)
        for line in text:
            if y < 45:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 45
            c.drawString(45, y, line[:105])
            y -= 14
        c.save()


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    paths = sorted(REPORTS_DIR.glob("eval_report_*.csv"))
    summaries = [summarize_variant(path) for path in paths]
    if not summaries:
        print("No eval reports found. Run python -m src.eval_runner first.")
        return
    write_ab_comparison(summaries)
    selected = summaries[-1]
    write_markdown_reports(selected)
    write_visual_dashboard(selected)
    write_architecture_png()
    write_pdf_reports()
    print(f"Wrote reports to {REPORTS_DIR}")


if __name__ == "__main__":
    main()
