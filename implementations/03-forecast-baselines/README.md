# 03: Forecasting baselines, scored the right way

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/03-forecast-baselines.ipynb)

Before any deep model or foundation model, beat these. Two synthetic series: a smooth fast mover and a lumpy slow mover.

```bash
python forecast.py
```

| Smooth series | MASE | 80% interval coverage |
|---|---|---|
| Naive | 1.49 | 23% |
| Seasonal naive | 0.90 | 77% |
| Moving average | 1.36 | 35% |
| Exponential smoothing | 1.30 | 27% |
| **Holt-Winters** | **0.60** | 69% |

## What to notice

- **Accuracy and calibration are different things.** Holt-Winters has the lowest error but its 80% intervals cover only 69% of outcomes. Safety stock built on those intervals will be too thin.
- **On lumpy demand, error metrics reward forecasting zero.** The naive forecast "wins" on the slow mover. Score spare parts and slow movers on stock-out and holding cost, not MASE.
- **A foundation model is optional here.** Install `chronos-forecasting` and the script adds a zero-shot Chronos-Bolt row, so you can see whether it beats the baselines on your own data.

Papers: [Chronos-2](https://arxiv.org/abs/2510.15821), [calibration of foundation models](https://arxiv.org/abs/2510.16060), [benchmarking challenges](https://arxiv.org/abs/2510.13654).
