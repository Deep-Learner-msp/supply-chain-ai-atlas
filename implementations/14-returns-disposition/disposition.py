"""
Returns disposition: decide at first touch on expected value, not "ship it all back".

20,000 returned items in three price bands. Each has a true condition grade:
  A like new  -> restock      B fixable -> refurbish
  C parts     -> recycle      D junk    -> scrap
The grade is uncertain where the item is first touched (store or carrier hub).
We know the customer's return reason and a quick 30-second inspection that
reads the right grade 70% of the time, otherwise a neighbouring grade.

Policies:
  Back to DC   : ship everything to the returns DC, grade it properly there,
                 then pick the best disposition. The common default.
  EV at first  : at first touch, compute the expected net value of each
  touch          option (restock on the spot, liquidate, recycle, scrap, or
                 ship to DC) from the grade probabilities, and pick the best.
  Oracle       : first touch with the true grade known (an upper bound).

All prices, costs and probabilities are synthetic and illustrative.

Run: python disposition.py
"""

import numpy as np

rng = np.random.default_rng(14)
N = 20_000
GRADES = "ABCD"
BANDS = {"Accessory": (18, 6.0), "Home goods": (70, 10.0), "Electronics": (350, 14.0)}  # price, ship to DC
REASONS = {  # share of returns, P(grade A, B, C, D)
    "Changed mind": (0.55, [0.75, 0.17, 0.06, 0.02]),
    "Defective": (0.30, [0.05, 0.45, 0.30, 0.20]),
    "Damaged": (0.15, [0.10, 0.30, 0.35, 0.25]),
}
DC_GRADE_COST = 4.0
LOCAL_COST = 1.0
INSPECT = np.array([[0.70, 0.30, 0.00, 0.00],   # P(inspection says column | true grade row)
                    [0.15, 0.70, 0.15, 0.00],
                    [0.00, 0.15, 0.70, 0.15],
                    [0.00, 0.00, 0.30, 0.70]])


def dc_value(price):
    """Net value per true grade once graded at the DC: restock, refurbish, recycle, scrap."""
    return np.array([0.90 * price - 3, 0.55 * price - (0.15 * price + 6), 0.08 * price - 1, -1.0])


def local_options(price):
    """Net value per true grade for each first-touch option (excluding the ship-to-DC option)."""
    return {
        "restock here": np.array([0.90 * price, -0.20 * price - 12, -0.30 * price - 12, -12.0]) - LOCAL_COST,
        "liquidate": np.array([0.30, 0.20, 0.05, 0.0]) * price - LOCAL_COST,
        "recycle": np.array([0.04, 0.04, 0.04, 0.0]) * price - LOCAL_COST,
        "scrap": np.array([-0.5] * 4),
    }


def main():
    band = rng.choice(list(BANDS), N, p=[0.5, 0.35, 0.15])
    reason = rng.choice(list(REASONS), N, p=[r[0] for r in REASONS.values()])
    true = np.array([rng.choice(4, p=REASONS[r][1]) for r in reason])
    seen = np.array([rng.choice(4, p=INSPECT[g]) for g in true])
    totals = {k: {"value": 0.0, "cost": 0.0, "to_dc": 0} for k in ["Back to DC", "EV at first touch", "Oracle"]}
    for i in range(N):
        price, ship = BANDS[band[i]]
        prior = np.array(REASONS[reason[i]][1])
        post = prior * INSPECT[:, seen[i]]
        post /= post.sum()
        dc_net = dc_value(price)
        options = {"ship to DC": dc_net - ship - DC_GRADE_COST, **local_options(price)}
        g = true[i]
        # Back to DC: always ship and grade, then best disposition for the true grade
        t = totals["Back to DC"]
        t["value"] += dc_net[g]
        t["cost"] += ship + DC_GRADE_COST
        t["to_dc"] += 1
        for policy, choice in [("EV at first touch", max(options, key=lambda k: post @ options[k])),
                               ("Oracle", max(options, key=lambda k: options[k][g]))]:
            t = totals[policy]
            cost = ship + DC_GRADE_COST if choice == "ship to DC" else LOCAL_COST
            t["value"] += options[choice][g] + cost
            t["cost"] += cost
            t["to_dc"] += choice == "ship to DC"
    print(f"{N:,} synthetic returns: " + ", ".join(f"{(band == b).mean():.0%} {b.lower()}" for b in BANDS) + "\n")
    print(f"{'Policy':<18} {'Recovered':>11} {'Handling':>10} {'Net':>11} {'Net/item':>9} {'Shipped to DC':>14}")
    print("-" * 78)
    for name, t in totals.items():
        net = t["value"] - t["cost"]
        print(f"{name:<18} {t['value']:>11,.0f} {t['cost']:>10,.0f} {net:>11,.0f} {net / N:>9.2f} "
              f"{t['to_dc'] / N:>14.0%}")
    b, e = totals["Back to DC"], totals["EV at first touch"]
    base, ev = b["value"] - b["cost"], e["value"] - e["cost"]
    print(f"\nDeciding at first touch recovers {1 - e['value'] / b['value']:.0%} less value, spends "
          f"{1 - e['cost'] / b['cost']:.0%} less on handling, and nets {ev - base:,.0f} more ({(ev - base) / base:+.0%}).")
    print("Most of the loss in returns is handling, not grading: stop paying to move items worth less "
          "than the trip.")

if __name__ == "__main__":
    main()
