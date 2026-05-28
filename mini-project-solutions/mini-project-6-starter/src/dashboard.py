from pathlib import Path


REPORTS_DIR = Path("reports")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # TODO(STAGE 3): Read eval_report_A.csv and eval_report_B.csv, then write ab_comparison.csv.
    # TODO(STAGE 4): Generate dashboard.png or dashboard.md with p95 latency, cost, refusal rate, and groundedness.
    (REPORTS_DIR / "dashboard.md").write_text(
        "# Dashboard\n\nTODO(STAGE 4): Fill this dashboard from evaluation results.\n",
        encoding="utf-8",
    )
    print(f"Wrote placeholder dashboard to {REPORTS_DIR / 'dashboard.md'}")


if __name__ == "__main__":
    main()

