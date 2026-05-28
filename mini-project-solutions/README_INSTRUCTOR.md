# Instructor Solution

Folder ini berisi full implementation dan generated artifacts.

Gunakan untuk:

- Reference saat debugging student.
- Membandingkan expected output.
- Membuat demo instructor.
- Mengambil potongan hint jika student stuck.

Jangan bagikan folder ini ke student sebelum mini project selesai.

Run:

```bash
pip install -r requirements.txt
python scripts\generate_sample_pdfs.py
python -m src.ingest
python scripts\smoke_test.py
python -m src.eval_runner --variant A
python -m src.eval_runner --variant B --top-k 6
python -m src.dashboard
uvicorn src.main:app --reload
```

Streamlit UI:

```bash
python -m streamlit run ui/streamlit_app.py
```

Gunakan UI ini untuk demo interaktif setelah FastAPI berjalan.
