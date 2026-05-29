# Stage TODO Guide

## Stage 1

Complete:

- `check_safety(query)` in `src/safety.py`.
- `read_document(path)` and `search(query)` in `src/retriever.py`.
- `generate(query, chunks)` in `src/generator.py`.
- `/chat` response and source mapping in `src/main.py`.

Acceptance:

- Normal after-sales query returns at least one source.
- Off-topic query is refused.
- Prompt injection query is refused.
- Streamlit UI can display answer, status, latency, refusal, and sources.

## Stage 2

Complete:

- JSONL logging in `src/logger.py`.
- BLEU-like, ROUGE-L, similarity metrics in `src/metrics.py`.
- Gold set loop in `src/eval_runner.py`.

Acceptance:

- `reports/eval_report_A.csv` exists.
- Report includes retrieval hit-rate, groundedness, refusal accuracy, latency, and cost.
- Queries sent from Streamlit are written to `logs/app.jsonl` after logging is implemented.

## Stage 3

Complete:

- Use `--variant` and `--top-k` in eval runner.
- Run the same gold set for Variant A and Variant B.
- Compare mean and standard deviation.

Acceptance:

- Only one variable changes.
- `reports/ab_comparison.csv` exists.

## Stage 4

Complete:

- `src/dashboard.py`.
- Cost calculation explanation.
- Demo script.

Acceptance:

- `dashboard.png` or `dashboard.md` exists.
- Cost/query is compared against IDR 250 target.
- Scaling plan to 100k queries/day is explained.
- Streamlit UI is used in the 5-minute demo.

## Stage 1 Status

Done in current code:

- Safety policy rejects toxic, injection, and off-topic queries.
- Retriever loads local documents (`pdf/csv/json/txt/md`), builds chunks, and ranks with lexical cosine similarity.
- Generator produces grounded baseline answer from retrieved evidence and includes source hints.
- FastAPI `/chat` returns source objects and status fields expected by UI/smoke test.
