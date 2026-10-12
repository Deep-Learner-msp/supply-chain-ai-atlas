"""
Forecasting baselines every supply chain model must beat, scored the right way.

Two synthetic weekly demand series (3 years):
  smooth : trend + yearly seasonality + noise (a fast mover)
  lumpy  : mostly zeros with occasional orders (a slow mover or spare part)

Methods: naive, seasonal naive, moving average, simple exponential smoothing,
Holt-Winters (additive), and Croston for the lumpy series.

Scores on the last 26 weeks:
  MASE     : error relative to seasonal naive in-sample (below 1.0 beats it)
  coverage : how often the true value fell inside the 80% interval
             (a well-calibrated model hits about 80%)

Optional: if `chronos-forecasting` is installed and the model can be
downloaded, a zero-shot Chronos-Bolt forecast is added.

Run: python forecast.py
"""

import numpy as np

H, SEASON = 26, 52
rng = np.random.default_rng(7)


def make_series():
    t = np.arange(3 * SEASON)
    smooth = 200 + 0.4 * t + 40 * np.sin(2 * np.pi * t / SEASON) + rng.normal(0, 12, len(t))
    lumpy = np.where(rng.random(len(t)) < 0.15, rng.poisson(20, len(t)), 0).astype(float)
    return {"smooth": np.maximum(smooth, 0), "lumpy": lumpy}


def naive(y, h): return np.repeat(y[-1], h)
def seasonal_naive(y, h): return np.array([y[-SEASON + (i % SEASON)] for i in range(h)])
def moving_avg(y, h, w=8): return np.repeat(y[-w:].mean(), h)


def ses(y, h, a=0.3):
    level = y[0]
    for v in y[1:]:
        level = a * v + (1 - a) * level
    return np.repeat(level, h)


def holt_winters(y, h, a=0.3, b=0.05, g=0.2, m=SEASON):
    level, trend = y[:m].mean(), (y[m:2 * m].mean() - y[:m].mean()) / m
    season = list(y[:m] - level)
    for i in range(m, len(y)):
        s = season[i - m]
        new_level = a * (y[i] - s) + (1 - a) * (level + trend)
        trend = b * (new_level - level) + (1 - b) * trend
        season.append(g * (y[i] - new_level) + (1 - g) * s)
        level = new_level
    n = len(y)
    return np.array([level + (k + 1) * trend + season[n - m + (k % m)] for k in range(h)])


def croston(y, h, a=0.1):
    nz = np.flatnonzero(y)
    if len(nz) == 0:
        return np.zeros(h)
    z, p, last = y[nz[0]], 1.0, nz[0]
    for idx in nz[1:]:
        z = a * y[idx] + (1 - a) * z
        p = a * (idx - last) + (1 - a) * p
        last = idx
    return np.repeat(z / p, h)


def mase(actual, pred, train):
    scale = np.mean(np.abs(train[SEASON:] - train[:-SEASON])) or 1.0
    return float(np.mean(np.abs(actual - pred)) / scale)


def coverage(method, train, actual):
    """80% interval from in-sample one-step residuals: simple and honest."""
    res = [train[cut] - method(train[:cut], 1)[0] for cut in range(len(train) - 52, len(train))]
    lo, hi = np.quantile(res, [0.1, 0.9])
    pred = method(train, len(actual))
    return float(np.mean((actual >= pred + lo) & (actual <= pred + hi)))


def try_chronos(train, test):
    try:
        import torch
        from chronos import BaseChronosPipeline
        pipe = BaseChronosPipeline.from_pretrained("amazon/chronos-bolt-small", device_map="cpu")
        q, _ = pipe.predict_quantiles(torch.tensor(train), prediction_length=H, quantile_levels=[0.1, 0.5, 0.9])
        lo, med, hi = (q[0, :, i].numpy() for i in range(3))
        return mase(test, med, train), float(np.mean((test >= lo) & (test <= hi)))
    except Exception:
        return None


METHODS = {"Naive": naive, "Seasonal naive": seasonal_naive, "Moving avg (8w)": moving_avg,
           "Exp. smoothing": ses, "Holt-Winters": holt_winters, "Croston": croston}
SKIP = {"smooth": {"Croston"}, "lumpy": {"Holt-Winters"}}


def main():
    for name, y in make_series().items():
        train, test = y[:-H], y[-H:]
        print(f"\n{name.upper()} series  (lower MASE is better; target coverage 80%)")
        print(f"{'Method':<20}{'MASE':>8}{'Coverage':>11}")
        for mname, f in METHODS.items():
            if mname in SKIP[name]:
                continue
            print(f"{mname:<20}{mase(test, f(train, H), train):>8.2f}{coverage(f, train, test):>10.0%}")
        chron = try_chronos(train, test)
        if chron:
            print(f"{'Chronos (zero-shot)':<20}{chron[0]:>8.2f}{chron[1]:>10.0%}")
        if name == "lumpy":
            print("Note: on lumpy demand, error metrics reward forecasting zero, so naive 'wins'."
                  "\nScore slow movers on stock-out and holding cost instead (see README).")
    print("\nRule: a new model ships only if it beats seasonal naive on MASE"
          "\nand its intervals cover about what they claim.")


if __name__ == "__main__":
    main()
