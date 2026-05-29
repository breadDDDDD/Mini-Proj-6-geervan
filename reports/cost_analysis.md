# Cost Analysis Report

## Source Files

- reports/eval_report_A.csv
- reports/eval_report_B.csv
- reports/ab_comparison.csv

## Pricing Assumptions

- Input: USD 0.15 / 1M tokens
- Output: USD 0.60 / 1M tokens
- Exchange rate: IDR 17,900 / USD
- Infra buffer: IDR 1.00 / query

## Formula

```text
cost_idr = ((input_tokens / 1_000_000) * 0.15 + (output_tokens / 1_000_000) * 0.60) * 17,900 + 1.00
```

## Current Result (from eval reports)

- Avg cost/query Variant A: IDR 3.7205
- Avg cost/query Variant B: IDR 3.7205
- p95 latency A/B: 1 ms
- Refusal accuracy A/B: 0.9143
- Groundedness A/B: 0.8000

## Projection

- 10,000 queries/day: IDR 37,205/day
- 100,000 queries/day: IDR 372,050/day

## Conclusion

Target <= IDR 250/query: PASS (actual ~IDR 3.7205/query).

