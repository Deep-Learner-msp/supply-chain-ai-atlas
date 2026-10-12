"""
ETA intervals that keep their promise: Gaussian vs split conformal.

Synthetic truckload lanes. Transit time depends on distance, carrier, a
peak-hour departure and a border crossing, plus noise. The noise is not
Gaussian: most trips are close to plan, but some hit weather, breakdowns or
long dwell, and border lanes hit them more often. That gives a long right tail.

One model (ordinary least squares, numpy only), two ways to put an interval
around its ETA:
  Gaussian  : ETA +/- z * sd of training residuals (assumes normal errors)
  Conformal : split conformal prediction. Hold out a calibration set and
              take the right order statistic of its residuals on each side
              (early and late), so the window can be lopsided like the
              delays. No distribution assumption; coverage is guaranteed on
              average if trips are exchangeable.

Both are scored on fresh test trips: coverage (share of trips that arrive
inside the window), the share that arrive after the window closes, and
the window width.

All data are synthetic and illustrative.

Run: python eta_conformal.py
"""

from statistics import NormalDist

import numpy as np

rng = np.random.default_rng(12)
N_TRAIN, N_CAL, N_TEST = 4000, 4000, 20000
LEVELS = [0.80, 0.90, 0.95, 0.99]
CARRIER_EFFECT = np.array([0.0, 1.5, -0.5, 3.0])  # hours


def make_trips(n):
    dist = rng.uniform(150, 2200, n)                    # km
    carrier = rng.integers(0, 4, n)
    peak = rng.random(n) < 0.3
    border = rng.random(n) < 0.25
    hours = 2 + dist / 65 + CARRIER_EFFECT[carrier] + 2.5 * peak + 4 * border
    noise = rng.normal(0, 1.2, n)
    delayed = rng.random(n) < np.where(border, 0.30, 0.08)
    noise += np.where(delayed, rng.exponential(10, n), 0.0)  # weather, breakdown, dwell
    X = np.column_stack([np.ones(n), dist, np.eye(4)[carrier][:, 1:], peak, border])
    return X, hours + noise


def main():
    X_tr, y_tr = make_trips(N_TRAIN)
    X_cal, y_cal = make_trips(N_CAL)
    X_te, y_te = make_trips(N_TEST)
    beta, *_ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    sd = np.std(y_tr - X_tr @ beta, ddof=X_tr.shape[1])
    cal_res = np.sort(y_cal - X_cal @ beta)
    pred = X_te @ beta
    res = y_te - pred
    print(f"Trips: {N_TRAIN:,} train, {N_CAL:,} calibration, {N_TEST:,} test. "
          f"Median transit {np.median(y_te):.1f} h, model MAE {np.abs(res).mean():.1f} h\n")
    print(f"{'':>6} {'Allowed':>8} | {'Gaussian':^22} | {'Conformal':^22}")
    print(f"{'Target':>6} {'late':>8} | {'cover':>6} {'late':>6} {'width':>8} | "
          f"{'cover':>6} {'late':>6} {'width':>8}")
    print("-" * 65)
    for level in LEVELS:
        tail = (1 - level) / 2
        half = NormalDist().inv_cdf(1 - tail) * sd
        g_lo, g_hi = -half, half
        k = int(np.ceil((N_CAL + 1) * (1 - tail)))  # split conformal rank, one per side
        c_lo, c_hi = cal_res[N_CAL - k], cal_res[k - 1]
        g_cov, g_late = np.mean((res >= g_lo) & (res <= g_hi)), np.mean(res > g_hi)
        c_cov, c_late = np.mean((res >= c_lo) & (res <= c_hi)), np.mean(res > c_hi)
        print(f"{level:>6.0%} {tail:>8.1%} | {g_cov:>6.1%} {g_late:>6.1%} {g_hi - g_lo:>6.1f} h | "
              f"{c_cov:>6.1%} {c_late:>6.1%} {c_hi - c_lo:>6.1f} h")
    print("\n(cover: share of trucks arriving inside the window; late: share arriving after it closes)")
    half = NormalDist().inv_cdf(0.995) * sd
    late = np.mean(res > half)
    print(f"With a 99% Gaussian window, {late:.1%} of trucks arrive after it closes, "
          f"{late / 0.005:.0f}x the 0.5% it promises.")
    k = int(np.ceil((N_CAL + 1) * 0.95))
    border = X_te[:, -1] == 1
    inside = (res >= cal_res[N_CAL - k]) & (res <= cal_res[k - 1])
    print(f"Caveat: the 90% conformal window covers {inside[border].mean():.0%} of border trips and "
          f"{inside[~border].mean():.0%} of the rest. Coverage is an average; calibrate per segment if you "
          "promise per segment.")
    print("Gaussian windows are too wide on normal days and too short in the late tail; "
          "conformal keeps the promise at every level.")


if __name__ == "__main__":
    main()
