# Evaluation Report

## Summary

- Total questions: 35
- Mean BLEU: 0.1163
- Mean ROUGE-L: 0.1473
- Mean embedding similarity: 0.2318
- Retrieval hit-rate: 100.0%
- Groundedness rate: 100.0%
- Refusal accuracy: 100.0%
- p50 latency: 0.0 ms
- p95 latency: 1.0 ms
- Mean cost/query: IDR 4.0971

## Method

The evaluator runs all gold questions against the same RAG pipeline, computes lexical quality metrics,
checks expected source retrieval, verifies groundedness, and records estimated cost and latency.
