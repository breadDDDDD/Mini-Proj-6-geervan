# Streamlit UI Run Guide

Streamlit UI dipakai agar student bisa mengetes chatbot secara interaktif tanpa harus memakai `curl`.

## Cara Menjalankan

Masuk ke folder student starter:

```bash
cd mini-project-6-starter
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Terminal 1, jalankan FastAPI:

```bash
uvicorn src.main:app --reload
```

Terminal 2, jalankan Streamlit:

```bash
python -m streamlit run ui/streamlit_app.py
```

Buka:

```text
http://localhost:8501
```

Default API URL di sidebar:

```text
http://127.0.0.1:8000
```

## Pemakaian per Stage

Stage 1:

- Gunakan UI untuk mengetes pertanyaan normal.
- Cek apakah answer muncul.
- Cek apakah sources muncul.
- Cek apakah prompt injection ditolak.

Stage 2:

- Kirim beberapa query dari UI.
- Cek apakah `logs/app.jsonl` bertambah.
- Jalankan `python -m src.eval_runner --variant A`.

Stage 3:

- Jalankan Variant A dan B dari terminal.
- Pakai UI untuk demo perbedaan behavior jika ada.

Stage 4:

- Gunakan UI sebagai bagian demo 5 menit.
- Tampilkan status, latency, refusal, dan sources dari UI.

