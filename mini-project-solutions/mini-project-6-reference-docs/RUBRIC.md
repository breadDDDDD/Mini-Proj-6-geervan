# Rubric - Mini Project 6

Total: 100 points.

| Criterion | What We Look For | Weight |
|---|---|---:|
| Working system | `/chat` returns grounded answers with sources, p95 target considered | 25 |
| Evaluation quality | BLEU/ROUGE/similarity/groundedness are computed and explained | 20 |
| Safety handling | Toxic, off-topic, prompt-injection, and leakage requests refused cleanly | 15 |
| A/B experiment | One-variable comparison, hypothesis, mean and standard deviation | 15 |
| Cost discipline | Cost/query, 10k/day, monthly estimate, 100k/day scaling plan | 15 |
| Demo + defense | Clear 5-minute demo, honest limitations, strong Q&A | 10 |

## Minimum Passing Evidence

- `/health` returns OK.
- `/chat` returns answer, sources, refusal flag, latency, and status.
- `eval_report.csv` exists.
- At least 5 adversarial queries are tested.
- A/B comparison changes one variable only.
- Cost/query is compared with IDR 250 target.

