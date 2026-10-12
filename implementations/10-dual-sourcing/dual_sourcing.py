"""
Single vs dual sourcing under disruption risk: average cost vs tail cost.

A brand needs 1,000 units a week for a year. Two suppliers:
  far  : offshore, 10.00 per unit, but a disruption (port closure, plant
         fire, sanctions) can stop it for 4 to 16 weeks
  near : nearshore, 12.50 per unit, rarely disrupted, and a contract can
         reserve surge capacity (fee per reserved unit per week)

Every unit not delivered is a lost sale that costs 25 in margin and
goodwill (on top of the purchase cost it would have had).

Policies:
  single far  : 100% from far
  single near : 100% from near
  dual 80/20  : 80% far, 20% near, plus reserved near capacity so near can
                ramp to 60% of demand while far is down

We simulate 20,000 years and report the mean annual cost and the 95th and
99th percentile years. All numbers are synthetic and illustrative.

Run: python dual_sourcing.py
"""

import numpy as np

rng = np.random.default_rng(10)
WEEKS, DEMAND, YEARS = 52, 1000, 20_000
PRICE = {"far": 10.00, "near": 12.50}
WEEKLY_HAZARD = {"far": 0.004, "near": 0.001}  # chance a disruption starts in a given week
LOST_SALE = 25.0
RESERVE_FEE = 0.40   # per reserved near unit per week
NEAR_SURGE = 0.60    # share of demand near can ship when far is down (dual policy)

POLICIES = {  # name: (far share, near share, reserved near capacity as share of demand)
    "Single far": (1.0, 0.0, 0.0),
    "Single near": (0.0, 1.0, 0.0),
    "Dual 80/20": (0.8, 0.2, NEAR_SURGE),
}


def outages(hazard):
    """Boolean array (YEARS, WEEKS): True when the supplier is down."""
    down = np.zeros((YEARS, WEEKS), dtype=bool)
    starts = rng.random((YEARS, WEEKS)) < hazard
    for y, w in zip(*np.nonzero(starts)):
        down[y, w:w + rng.integers(4, 17)] = True
    return down


def annual_cost(far_share, near_share, reserve, far_down, near_down):
    far_units = np.where(far_down, 0.0, far_share * DEMAND)
    near_cap = max(near_share, reserve) * DEMAND
    near_wanted = np.where(far_down, near_cap, near_share * DEMAND)
    near_units = np.where(near_down, 0.0, near_wanted)
    lost = DEMAND - far_units - near_units
    weekly = (far_units * PRICE["far"] + near_units * PRICE["near"] + lost * LOST_SALE
              + max(reserve - near_share, 0.0) * DEMAND * RESERVE_FEE)
    return weekly.sum(axis=1)


def main():
    far_down, near_down = outages(WEEKLY_HAZARD["far"]), outages(WEEKLY_HAZARD["near"])
    print(f"Simulated years: {YEARS:,}. Far supplier disrupted in "
          f"{far_down.any(axis=1).mean():.0%} of years, near in {near_down.any(axis=1).mean():.0%}.\n")
    print(f"{'Policy':<12} {'Mean cost':>11} {'P95 cost':>11} {'P99 cost':>11} {'Worst year':>11}")
    print("-" * 60)
    results = {}
    for name, (fs, ns, res) in POLICIES.items():
        cost = annual_cost(fs, ns, res, far_down, near_down)
        mean, p95, p99 = cost.mean(), *np.percentile(cost, [95, 99])
        results[name] = (mean, p95, p99)
        print(f"{name:<12} {mean:>11,.0f} {p95:>11,.0f} {p99:>11,.0f} {cost.max():>11,.0f}")
    (m1, p1, q1), (m2, p2, q2) = results["Single far"], results["Dual 80/20"]
    print(f"\nDual sourcing costs {m2 - m1:,.0f} more in an average year ({(m2 - m1) / m1:+.1%}) "
          f"and {p1 - p2:,.0f} less in a 1-in-20 bad year ({(p2 - p1) / p1:+.1%}).")
    print("Judge sourcing on the bad years, not the average one: dual sourcing is insurance.")


if __name__ == "__main__":
    main()
