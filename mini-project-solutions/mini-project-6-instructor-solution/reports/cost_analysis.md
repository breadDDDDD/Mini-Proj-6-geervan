# Cost Analysis

## Result

- Mean cost/query: IDR 4.0971
- Daily cost at 10k queries: IDR 40,971
- Monthly cost at 10k/day: IDR 1,229,130
- Target: <= IDR 250/query
- Status: PASS

## Formula

Input and output token estimates are multiplied by the configured model prices:

```text
input_tokens / 1,000,000 * INPUT_USD_PER_1M_TOKENS * IDR_PER_USD
output_tokens / 1,000,000 * OUTPUT_USD_PER_1M_TOKENS * IDR_PER_USD
```

Local retrieval and rule-based safety do not add per-query model cost.
