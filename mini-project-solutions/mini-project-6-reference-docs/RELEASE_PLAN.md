# Release Plan untuk Student

Tujuan release plan ini adalah membantu student tanpa memberikan semua jawaban.

## Paket yang Dibagikan

Bagikan hanya:

```text
mini-project-6-starter/
```

Jangan bagikan:

```text
mini-project-6-instructor-solution/
mini-project-6-reference-docs/INSTRUCTOR_ANSWER_KEY.md
```

## Cara Release Bertahap

### Sebelum Kelas

Bagikan starter project dan brief PDF.

Student boleh menjalankan:

```bash
pip install -r requirements.txt
python scripts\generate_sample_pdfs.py
python -m src.ingest
uvicorn src.main:app --reload
python -m streamlit run ui/streamlit_app.py
```

Expected: API dan UI menyala, tetapi retrieval dan metrics belum lengkap.

### Hour 1

Fokus:

- Safety filter.
- Document loading.
- Chunking.
- Retrieval.
- `/chat` response with sources.
- Streamlit UI menampilkan answer, status, latency, refusal, dan sources.

Instructor boleh memberi hint, bukan copy-paste solution.

### Hour 2

Fokus:

- Structured logging.
- Evaluation runner.
- Quality metrics.
- Retrieval hit-rate and groundedness.

### Hour 3

Fokus:

- Variant A vs Variant B.
- Satu variabel berubah.
- Mean and standard deviation.

### Hour 4

Fokus:

- Cost analysis.
- Dashboard.
- Streamlit UI untuk demo interaktif.
- Architecture explanation.
- 5-minute demo.

## Batas Bantuan Instructor

Boleh:

- Menjelaskan konsep.
- Menunjukkan acceptance criteria.
- Memberi pseudo-code singkat.
- Membantu debugging error environment.

Jangan:

- Memberikan `mini-project-6-instructor-solution`.
- Memberikan full implementation file.
- Mengizinkan hardcoded gold answers.
