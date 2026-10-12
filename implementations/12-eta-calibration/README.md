# 12: ETA intervals, and why Gaussian windows break their promise in the tail

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/12-eta-calibration.ipynb)

Synthetic truckload lanes: transit time depends on distance, carrier, peak-hour departure and border crossing. Most trips run close to plan; some hit weather, breakdowns or long dwell, which gives a long late tail. One least-squares model (numpy only), two ways to put a window around its ETA, scored on 20,000 fresh test trips. Synthetic, illustrative data.

```bash
pip install numpy
python eta_conformal.py
```

| Target | Allowed late | Gaussian cover | Gaussian late | Gaussian width | Conformal cover | Conformal late | Conformal width |
|---|---|---|---|---|---|---|---|
| 80% | 10.0% | 94.0% | 6.0% | 12.8 h | 80.0% | 10.3% | 5.0 h |
| 90% | 5.0% | 95.1% | 4.9% | 16.4 h | 89.8% | 5.0% | 11.7 h |
| 95% | 2.5% | 95.8% | 4.2% | 19.6 h | 94.6% | 2.7% | 18.6 h |
| 99% | 0.5% | 96.8% | 3.2% | 25.7 h | 98.9% | 0.4% | 37.9 h |

Cover is the share of trucks arriving inside the window; late is the share arriving after it closes.

- **Gaussian**: ETA plus or minus z times the standard deviation of training residuals.
- **Conformal**: [split conformal prediction](https://arxiv.org/abs/2107.07511). Hold out a calibration set and use its residual order statistics on each side as the window edges. No distribution assumption.

## What to notice

- The Gaussian window is wrong in both directions. At 80% it covers 94% of trips with a window 2.5 times wider than needed. At 99% it lets 3.2% of trucks arrive late, 6 times the 0.5% it promises.
- Heavy, one-sided delays break the normal assumption: the long tail inflates the standard deviation (too wide on normal days) while the tail itself is longer still (too short where it matters).
- Conformal hits the target at every level using the same model. It only changes how the window is computed, from held-out data.
- An honest 99% window here is 38 hours wide. That is the real uncertainty of these lanes; the narrower Gaussian window hides it.
- Conformal coverage is an average over all trips. The 90% window covers 71% of border trips and 96% of the rest. If you promise per segment, calibrate per segment.
