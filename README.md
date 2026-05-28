# Mini Project 6 Starter - LLM Monitoring Dashboard Azure-Free

Starter ini dibuat agar student **tidak mulai dari nol**, tetapi tetap mengerjakan bagian penting dari mini project:

- RAG retrieval.
- Safety filter.
- Structured logging.
- Evaluation metrics.
- A/B experiment.
- Cost/dashboard report.

Beberapa file sudah lengkap, beberapa file berisi `TODO(STAGE X)`. Kerjakan TODO sesuai urutan stage.

## Setup

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

Jalankan API di terminal pertama:

```bash
powershell -ExecutionPolicy Bypass -File scripts\run_api.ps1
```

Atau langsung:

```bash
uvicorn src.main:app --reload
```

Jalankan UI di terminal kedua:

```bash
python -m streamlit run ui/streamlit_app.py
```

Buka URL Streamlit yang muncul, biasanya:

```text
http://localhost:8501
```

UI akan memanggil FastAPI di:

```text
http://127.0.0.1:8000
```

Jika port API berbeda, ubah field `FastAPI URL` di sidebar Streamlit.

## Stage 1 - Baseline RAG

Goal:

- `/health` berjalan.
- `/chat` menerima pertanyaan ID/EN.
- Sistem melakukan retrieval dari dokumen lokal.
- Response berisi `answer`, `sources`, `refusal`, `latency_ms`, dan `status`.

Kerjakan TODO di:

- `src/safety.py`
- `src/retriever.py`
- `src/generator.py`
- `src/main.py`

Test:

```bash
python scripts\smoke_test.py
```

Test interaktif:

```bash
uvicorn src.main:app --reload
python -m streamlit run ui/streamlit_app.py
```

## Stage 2 - Monitoring & Evaluation

Goal:

- Request tercatat ke `logs/app.jsonl`.
- Evaluasi membaca `data/gold_questions.csv`.
- Report CSV terbentuk.
- Metrik utama bisa dijelaskan.

Kerjakan TODO di:

- `src/logger.py`
- `src/metrics.py`
- `src/eval_runner.py`

Run:

```bash
python -m src.eval_runner --variant A
```

## Stage 3 - A/B Experiment

Goal:

- Jalankan Variant A dan B pada gold set yang sama.
- Ubah satu variabel saja, misalnya `top_k`.
- Buat comparison report.

Run:

```bash
python -m src.eval_runner --variant A
python -m src.eval_runner --variant B --top-k 6
python -m src.dashboard
```

## Stage 4 - Cost Report & Demo

Goal:

- Buat dashboard.
- Hitung cost/query.
- Siapkan demo 5 menit.

Kerjakan TODO di:

- `src/dashboard.py`
- `docs/COST_ANALYSIS.md`
- `docs/DEMO_SCRIPT.md`

Expected final artifacts:

- `reports/eval_report_A.csv`
- `reports/eval_report_B.csv`
- `reports/ab_comparison.csv`
- `reports/dashboard.png`
- `reports/cost_analysis.pdf` atau `reports/cost_analysis.md`

## Rule

Jangan hardcode jawaban untuk gold questions. Sistem harus mengambil evidence dari dokumen lokal.
