# Cost Analysis

## Assumptions

- Model input price: USD 0.15 / 1M tokens.
- Model output price: USD 0.60 / 1M tokens.
- Exchange rate: IDR 16,200 / USD.
- Average input: 1,100 tokens.
- Average output: 180 tokens.
- Embedding/vector search: local, no per-token API cost.
- Safety: rule-based, no model call.

## Formula

Input:

```text
1,100 / 1,000,000 * USD 0.15 * IDR 16,200 = IDR 2.67
```

Output:

```text
180 / 1,000,000 * USD 0.60 * IDR 16,200 = IDR 1.75
```

Total:

```text
IDR 2.67 + IDR 1.75 + IDR 1.00 infra/log buffer = IDR 5.42/query
```

## 10k Queries/Day

```text
IDR 5.42 * 10,000 = IDR 54,200/day
```

## 100k Queries/Day

```text
IDR 5.42 * 100,000 = IDR 542,000/day
```

## Conclusion

Target `<= IDR 250/query`; estimated `IDR 5.42/query`. Status: PASS.

