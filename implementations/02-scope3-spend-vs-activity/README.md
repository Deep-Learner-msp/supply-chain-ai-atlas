# 02: Scope 3, spend-based vs activity-based

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/02-scope3-spend-vs-activity.ipynb)

Why a supplier can halve its emissions and look worse in its customer's climate report.

```bash
python compare.py
```

| Year | Supplier | Spend | Reported (spend-based) | Real (activity-based) |
|---|---|---|---|---|
| 1 | Anita, grid power | $1,000,000 | 600 t | 600 t |
| 2 | Anita, solar | $1,050,000 | 630 t | 300 t |
| 3 | Rival, coal | $950,000 | 570 t | 720 t |

Anita goes solar: real emissions fall 50%, reported emissions rise 5%. The switch to coal: real emissions rise 140%, reported emissions fall 10%.

All numbers are illustrative. The mechanism is real: spend-based accounting multiplies what you paid by one industry-average factor, so it tracks invoices, not factories.

## Where AI fits

See [docs/lifecycle/08-cross-cutting.md](../../docs/lifecycle/08-cross-cutting.md): document AI for activity data, gap-filling models with uncertainty, agents for supplier follow-up, and exchange standards such as WBCSD PACT.
