# Teaching Notes - Mini Project 6

Gunakan repo ini sebagai instructor solution dan starter reference.

## Cara Menggunakan di Kelas

1. Minta student menjalankan baseline dengan `GENERATOR_MODE=fake`.
2. Setelah pipeline benar, minta mereka mengganti provider ke OpenAI-compatible endpoint.
3. Tekankan bahwa yang dinilai bukan hanya jawaban chatbot, tetapi juga measurement discipline.
4. A/B experiment harus mengubah satu variabel saja.
5. Semua angka cost harus ditunjukkan dengan rumus.
6. Gunakan Streamlit UI untuk demo interaktif, tetapi tetap minta student membuktikan metric dari evaluator.

## Checkpoint per Hour

Hour 1:

- `/health` berjalan.
- `/chat` menjawab dengan sources.
- Streamlit UI berjalan dan menampilkan sources.
- Unsafe/off-topic query ditolak.

Hour 2:

- `logs/app.jsonl` terbentuk.
- `eval_report_A.csv` terbentuk.
- Summary metrik bisa dijelaskan.

Hour 3:

- Variant A dan B dijalankan pada gold set yang sama.
- `ab_comparison.csv` terbentuk.
- Student dapat menjelaskan pemenang dan trade-off.

Hour 4:

- Student menunjukkan dashboard, cost analysis, architecture, dan demo script.
- Student dapat menjawab pertanyaan scaling ke 100k query/hari.
