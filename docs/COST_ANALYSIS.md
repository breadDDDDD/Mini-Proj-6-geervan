# Cost Analysis

## Scope and Inputs

Dokumen ini memakai hasil evaluasi aktual dari:

- `reports/eval_report_A.csv`
- `reports/eval_report_B.csv`
- `reports/ab_comparison.csv`

Ringkasan metrik dari report:

- Average cost/query Variant A: **IDR 3.7205**
- Average cost/query Variant B: **IDR 3.7205**
- p95 latency A/B: **1 ms**
- Refusal accuracy A/B: **0.9143**
- Groundedness rate A/B: **0.8000**

## Cost Formula

Per query:

```text
cost_idr = ((input_tokens / 1_000_000) * input_usd_per_1m_tokens
          + (output_tokens / 1_000_000) * output_usd_per_1m_tokens) * idr_per_usd
          + infra_buffer_idr
```

Implementasi formula ada di `src/costing.py`.

Parameter default dari `src/config.py`:

- Input price: USD 0.15 / 1M tokens
- Output price: USD 0.60 / 1M tokens
- Exchange rate: IDR 16,200 / USD
- Infra/log buffer: IDR 1.00 per query

## Daily Projection

Menggunakan rata-rata biaya report (`IDR 3.7205/query`):

- 10,000 query/hari: `3.7205 * 10,000 = IDR 37,205/hari`
- 100,000 query/hari: `3.7205 * 100,000 = IDR 372,050/hari`

## Target Check

Target biaya adalah `<= IDR 250/query`.

- Aktual Variant A: `IDR 3.7205/query`
- Aktual Variant B: `IDR 3.7205/query`

Status: **PASS**.

## Notes

- Pada data evaluasi saat ini, perbedaan `top_k` (A=4, B=6) belum mengubah metrik biaya/latensi/quality secara signifikan.
- Perbaikan kualitas berikutnya kemungkinan lebih berdampak jika indeks/chunking retrieval ditingkatkan, bukan hanya menaikkan `top_k`.
