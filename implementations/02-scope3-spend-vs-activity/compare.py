"""
Scope 3: spend-based vs activity-based accounting.

A shampoo brand buys 2 million plastic bottles a year. Three years:

  Year 1  Supplier A (Anita) on grid power.
  Year 2  Anita moves to solar: real emissions per bottle halve, price rises 5%.
  Year 3  Procurement switches to Supplier B, a cheaper coal-powered plant.

Spend-based method : emissions = spend x one industry-average factor (kg CO2e per $)
Activity-based     : emissions = bottles x the supplier's own kg CO2e per bottle

All numbers are illustrative. The mechanism is the point.

Run: python compare.py
"""

BOTTLES = 2_000_000
INDUSTRY_FACTOR = 0.60  # kg CO2e per $ spent, one average for every supplier

years = [
    # label, supplier, price per bottle ($), real kg CO2e per bottle
    ("Year 1", "Anita, grid power", 0.500, 0.30),
    ("Year 2", "Anita, solar", 0.525, 0.15),
    ("Year 3", "Rival, coal", 0.475, 0.36),
]


def tonnes(kg: float) -> float:
    return kg / 1000


def main() -> None:
    print(f"{'':<8}{'Supplier':<20}{'Spend':>12}{'Spend-based':>14}{'Real':>10}")
    print(f"{'':<8}{'':<20}{'':>12}{'(reported t)':>14}{'(t)':>10}")
    rows = []
    for label, who, price, kg_per_bottle in years:
        spend = BOTTLES * price
        reported = tonnes(spend * INDUSTRY_FACTOR)
        real = tonnes(BOTTLES * kg_per_bottle)
        rows.append((reported, real))
        print(f"{label:<8}{who:<20}{'$' + format(spend, ',.0f'):>12}{reported:>14,.0f}{real:>10,.0f}")

    (r1, a1), (r2, a2), (r3, a3) = rows
    print("\nAnita goes solar  : real", f"{(a2 / a1 - 1) * 100:+.0f}%", "| reported", f"{(r2 / r1 - 1) * 100:+.0f}%")
    print("Switch to coal    : real", f"{(a3 / a2 - 1) * 100:+.0f}%", "| reported", f"{(r3 / r2 - 1) * 100:+.0f}%")
    print("\nThe spend-based number tracks the invoice, not the factory.")


if __name__ == "__main__":
    main()
