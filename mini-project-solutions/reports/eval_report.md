# Evaluation Report

## Summary

- Total questions: 35
- Mean BLEU: 0.2998
- Mean ROUGE-L: 0.3733
- Mean embedding similarity: 0.5093
- Retrieval hit-rate: 100.0%
- Groundedness rate: 100.0%
- Refusal accuracy: 100.0%
- p50 latency: 508.0 ms
- p95 latency: 1413.0 ms
- Mean cost/query: IDR 4.0258

## Method

The evaluator runs all gold questions against the same RAG pipeline, computes lexical quality metrics,
checks expected source retrieval, verifies groundedness, and records estimated cost and latency.
