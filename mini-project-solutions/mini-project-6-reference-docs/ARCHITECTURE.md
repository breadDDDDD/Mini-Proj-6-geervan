# Architecture

```mermaid
flowchart LR
    U[User ID/EN] --> API[FastAPI /chat]
    API --> S[Safety Filter]
    S -->|unsafe/off-topic| R[Safe Refusal]
    S -->|allowed| RET[Retriever]
    D[(Local Documents)] --> ING[Ingest + Chunk]
    ING --> V[(Local TF-IDF Index)]
    RET --> V
    RET --> P[Grounded Prompt]
    P --> G[Generator]
    G --> OUT[Answer + Sources]
    OUT --> LOG[JSONL Logs]
    LOG --> EVAL[Evaluation Runner]
    EVAL --> DASH[Dashboard + Reports]
```

## Components

- FastAPI: serving `/health` and `/chat`.
- Safety filter: blocks toxic, off-topic, prompt-injection, and system leakage requests.
- Retriever: local lexical TF-IDF search over chunked local documents.
- Generator: fake extractive generator by default, or OpenAI-compatible API.
- Logger: JSONL structured logs with request ID, latency, token estimate, retrieval stats, and refusal reason.
- Evaluation: gold set runner with quality, safety, latency, and cost metrics.

