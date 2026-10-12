# 09: Safety stock, and why demand noise is the small part

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/09-safety-stock.ipynb)

One DC item: 100 units a day (standard deviation 25), a quoted 10-day lead time that really varies (standard deviation 3 days, skewed late). Two textbook safety stock formulas, checked against 200,000 simulated replenishment cycles. Synthetic, illustrative data.

```bash
pip install numpy
python safety_stock.py
```

| Target service level | Demand-only SS | Achieved | Combined SS | Achieved |
|---|---|---|---|---|
| 90% | 101 | 66.1% | 398 | 89.3% |
| 95% | 130 | 69.3% | 510 | 93.7% |
| 98% | 162 | 72.5% | 637 | 96.7% |
| 99% | 184 | 74.5% | 722 | 98.0% |

Demand-only: `SS = z * sigma_d * sqrt(L)`. Combined: `SS = z * sqrt(L * sigma_d^2 + d^2 * sigma_L^2)` ([formula and assumptions](https://en.wikipedia.org/wiki/Safety_stock)). Reorder point = `d * L + SS`.

## What to notice

- The demand-only formula promises 95% and delivers 69%. It is not a little off; it ignores the term that matters.
- Here lead-time variability causes 94% of the variance of lead-time demand. Three days of lead-time noise outweighs a 25% daily demand swing.
- The combined formula gets close but still lands a point or two short, because real lead times are skewed (a few very late deliveries) and the formula assumes a normal shape. Simulate your own lead-time history before trusting any formula at 99%.
- Cutting lead-time variability with the supplier is usually cheaper than holding four times the stock.
