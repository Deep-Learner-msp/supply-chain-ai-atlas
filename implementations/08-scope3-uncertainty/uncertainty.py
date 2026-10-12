"""
Scope 3 with honest uncertainty, and which supplier to chase first.

A brand buys from 12 suppliers. For each, the emissions estimate comes from
one of three data sources, each with its own uncertainty:

  primary   : the supplier's own measured data        (about +/-10%)
  modelled  : ML estimate from similar suppliers      (about +/-35%)
  spend     : spend x industry-average factor         (about +/-70%)

A Monte Carlo simulation gives the total with a 90% interval instead of one
false-precise number. Then it ranks suppliers by how much of the total's
uncertainty they cause: the first email to send.

All numbers are illustrative.

Run: python uncertainty.py
"""

import numpy as np

rng = np.random.default_rng(11)
SPREAD = {"primary": 0.10, "modelled": 0.35, "spend": 0.70}  # approx. one standard deviation, log scale

SUPPLIERS = [  # name, central estimate (t CO2e), data source
    ("Bottles A", 600, "primary"), ("Bottles B", 420, "spend"), ("Caps", 90, "spend"),
    ("Labels", 60, "modelled"), ("Surfactants", 1300, "spend"), ("Fragrance", 210, "modelled"),
    ("Cartons", 340, "primary"), ("Pallets", 75, "spend"), ("Freight in", 520, "modelled"),
    ("Co-packer", 1500, "primary"), ("Film wrap", 45, "modelled"), ("Glue", 30, "spend"),
]
N = 20_000


def simulate(suppliers):
    draws = np.column_stack([
        est * rng.lognormal(-SPREAD[src] ** 2 / 2, SPREAD[src], N) for _, est, src in suppliers
    ])
    return draws


def summary(draws):
    total = draws.sum(axis=1)
    lo, mid, hi = np.percentile(total, [5, 50, 95])
    return lo, mid, hi


def main():
    draws = simulate(SUPPLIERS)
    lo, mid, hi = summary(draws)
    point = sum(e for _, e, _ in SUPPLIERS)
    share = sum(e for _, e, s in SUPPLIERS if s == "primary") / point
    print(f"Single number most reports show : {point:,.0f} t CO2e")
    print(f"Honest range (90%)              : {lo:,.0f} to {hi:,.0f} t  (median {mid:,.0f})")
    print(f"Share of total from primary data: {share:.0%}\n")

    total = draws.sum(axis=1)
    contrib = []
    for i, (name, est, src) in enumerate(SUPPLIERS):
        contrib.append((np.cov(draws[:, i], total)[0, 1] / total.var(), name, est, src))
    contrib.sort(reverse=True)
    print("Who causes the uncertainty (share of variance of the total):")
    for c, name, est, src in contrib[:5]:
        print(f"  {name:<12} {c:>5.0%}   ({src}, est. {est} t)")

    target = contrib[0][1]
    upgraded = [(n, e, "primary" if n == target else s) for n, e, s in SUPPLIERS]
    lo2, _, hi2 = summary(simulate(upgraded))
    print(f"\nGet primary data from {target} alone and the range narrows from "
          f"{hi - lo:,.0f} t wide to {hi2 - lo2:,.0f} t wide.")
    print("Chase the supplier who causes the most uncertainty, not the biggest or the easiest.")


if __name__ == "__main__":
    main()
