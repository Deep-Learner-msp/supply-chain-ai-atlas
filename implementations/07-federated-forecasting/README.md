# 07: Federated demand forecasting, and where it breaks

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/07-federated-forecasting.ipynb)

Three retailers, 30 weeks of data each, no raw data shared.

```bash
python federated.py
```

| Test error (MSE) | Local | Federated | Centralized | Personalized |
|---|---|---|---|---|
| Same market, retailer A | 89 | **80** | 80 | 88 |
| Price shock, retailer C | 72 | 154 | 156 | **68** |

## What to notice

- **When partners look alike,** federated learning matches pooling all the data, without anyone sharing it.
- **When one partner hits a shock,** the shared model blurs it. Retailer C's error doubles.
- **Personalization** (federated model plus a few local training steps) recovers it. Shared models need a local layer, because the partner who looks different is often the one seeing the shock first.

Papers: [PA-CFL](https://arxiv.org/abs/2503.12220), [Federated ensemble forecasting under volatility](https://arxiv.org/abs/2608.21399).
