# Mini Project 6 - LLM Monitoring Dashboard Azure-Free

Starter solution untuk mini project RAG assistant after-sales Mitsubishi. Project ini sengaja dibuat **Azure-free**: dokumen lokal, vector search lokal, safety rule-based, logging JSONL, dan provider LLM yang bisa diganti melalui OpenAI-compatible endpoint.

Default mode memakai `GENERATOR_MODE=fake`, jadi aplikasi tetap bisa berjalan tanpa API key. Untuk memakai LLM sungguhan, ubah `GENERATOR_MODE=openai_compatible` dan isi `LLM_API_KEY`.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts\generate_sample_pdfs.py
python -m src.ingest
uvicorn src.main:app --reload
```

## Chatbot UI dengan Streamlit

Terminal 1, jalankan API:

```bash
uvicorn src.main:app --reload
```

Terminal 2, jalankan UI:

```bash
python -m streamlit run ui/streamlit_app.py
```

Buka:

```text
http://localhost:8501
```

UI akan memanggil `/health` dan `/chat` dari FastAPI default `http://127.0.0.1:8000`.

Cek API:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Berapa interval servis Xpander?\",\"session_id\":\"demo-001\"}"
```

## Evaluation dan Reports

Jalankan evaluasi terhadap gold set:

```bash
python -m src.eval_runner --variant A
python -m src.eval_runner --variant B --top-k 6
python -m src.dashboard
```

Output utama:

- `logs/app.jsonl`
- `reports/eval_report_A.csv`
- `reports/eval_report_B.csv`
- `reports/ab_comparison.csv`
- `reports/dashboard.png`
- `reports/eval_report.pdf`
- `reports/cost_analysis.pdf`

## Project Scope

Yang dibangun:

- `/health` endpoint.
- `/chat` endpoint.
- Local document loader untuk PDF/TXT/CSV/JSON.
- Lightweight TF-IDF vector retrieval.
- Safety filter untuk toxic, prompt injection, system prompt leakage, dan off-topic.
- Provider abstraction: fake generator dan OpenAI-compatible generator.
- Structured JSONL logging.
- Evaluation runner: BLEU-like, ROUGE-L, METEOR-like, embedding/token similarity, groundedness, retrieval hit-rate, refusal rate, latency, cost.
- Dashboard dan report generator.

## API Contract

Request:

```json
{
  "query": "What is covered by warranty?",
  "session_id": "demo-001"
}
```

Response:

```json
{
  "answer": "Warranty coverage follows the warranty terms document...",
  "sources": [
    {
      "filename": "warranty_terms.pdf",
      "chunk_id": "warranty_terms.pdf:1",
      "score": 0.72
    }
  ],
  "refusal": false,
  "latency_ms": 820,
  "status": "ok"
}
```

## A/B Experiment

Default comparison:

- Variant A: `TOP_K=4`
- Variant B: `TOP_K=6`

Hypothesis: menaikkan `TOP_K` akan memperbaiki retrieval hit-rate dan groundedness, dengan trade-off latency dan token cost.

## Submission Checklist

- `src/` lengkap.
- `README.md` berisi setup dan run steps.
- `.env.example` tanpa API key asli.
- `eval_report.pdf`.
- `dashboard.png`.
- `architecture.png`.
- `cost_analysis.pdf`.
- A/B experiment hanya mengubah satu variabel.
