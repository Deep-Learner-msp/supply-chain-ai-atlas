"""
Safety stock when the lead time moves, not just the demand.

A DC item sells about 100 units a day (standard deviation 25). The supplier
quotes 10 days, but real lead times vary: standard deviation 3 days, with a
right skew (a few very late deliveries).

Two textbook safety stock formulas for a reorder point policy:
  demand only : SS = z * sigma_d * sqrt(L)
  combined    : SS = z * sqrt(L * sigma_d^2 + d^2 * sigma_L^2)
Reorder point = d * L + SS.

We simulate 200,000 replenishment cycles (random lead time, random daily
demand) and count how often demand during the lead time stays below the
reorder point. That is the cycle service level the formula promised.

All numbers are synthetic and illustrative.

Run: python safety_stock.py
"""

from statistics import NormalDist

import numpy as np

rng = np.random.default_rng(9)
D, SIGMA_D = 100.0, 25.0  # units per day
L, SIGMA_L = 10.0, 3.0    # days
TARGETS = [0.90, 0.95, 0.98, 0.99]
CYCLES = 200_000


def simulate_ddlt(cycles):
    # Gamma lead time: mean L, standard deviation SIGMA_L, skewed to the right
    shape = (L / SIGMA_L) ** 2
    lead = rng.gamma(shape, L / shape, cycles)
    # Sum of `lead` days of iid normal daily demand
    return rng.normal(D * lead, SIGMA_D * np.sqrt(lead))


def safety_stocks(z):
    demand_only = z * SIGMA_D * np.sqrt(L)
    combined = z * np.sqrt(L * SIGMA_D ** 2 + D ** 2 * SIGMA_L ** 2)
    return demand_only, combined


def main():
    ddlt = simulate_ddlt(CYCLES)
    print(f"Demand {D:.0f}/day (sd {SIGMA_D:.0f}), lead time {L:.0f} days (sd {SIGMA_L:.0f}), "
          f"{CYCLES:,} simulated cycles\n")
    print(f"{'Target':>7} | {'Demand-only SS':>14} {'achieved':>9} | {'Combined SS':>11} {'achieved':>9}")
    print("-" * 60)
    for target in TARGETS:
        z = NormalDist().inv_cdf(target)
        ss_d, ss_c = safety_stocks(z)
        hit_d = np.mean(ddlt <= D * L + ss_d)
        hit_c = np.mean(ddlt <= D * L + ss_c)
        print(f"{target:>7.0%} | {ss_d:>14,.0f} {hit_d:>9.1%} | {ss_c:>11,.0f} {hit_c:>9.1%}")
    share = D ** 2 * SIGMA_L ** 2 / (L * SIGMA_D ** 2 + D ** 2 * SIGMA_L ** 2)
    print(f"\nShare of lead-time demand variance caused by lead-time variability: {share:.0%}")
    z = NormalDist().inv_cdf(0.95)
    ss_d, ss_c = safety_stocks(z)
    print(f"At a 95% target the demand-only formula holds {ss_d:.0f} units and delivers "
          f"{np.mean(ddlt <= D * L + ss_d):.0%}; the combined formula holds {ss_c:.0f} and delivers "
          f"{np.mean(ddlt <= D * L + ss_c):.0%}.")
    print("Lead-time variability, not demand noise, drives most of the safety stock you need.")


if __name__ == "__main__":
    main()
