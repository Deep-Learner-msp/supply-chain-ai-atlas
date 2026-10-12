"""
Bullwhip effect simulator.

A four-tier chain (Store -> DC -> Brand -> Supplier). Shoppers buy 100 units a
week, then 5% more for five weeks (a hot spell), then back to 100.

Each tier uses a standard order-up-to policy with a moving-average forecast.
Two scenarios:

  no_sharing : each tier forecasts from the orders it receives from the tier below
  sharing    : each tier forecasts from real shopper demand (point-of-sale data)

Run:  python simulate.py
Out:  prints peak swing per tier and writes bullwhip.png next to this file.
"""

from pathlib import Path

import numpy as np

TIERS = ["Store", "DC", "Brand", "Supplier"]
WEEKS = 40
LEAD_TIME = 2      # weeks between placing an order and receiving it
WINDOW = 4         # weeks in the moving-average forecast


def shopper_demand(weeks: int = WEEKS) -> np.ndarray:
    d = np.full(weeks, 100.0)
    d[10:15] = 105.0  # the hot spell: +5%
    return d


def order_up_to(incoming: np.ndarray, signal: np.ndarray) -> np.ndarray:
    """Orders placed by one tier.

    incoming : orders this tier must fill each week
    signal   : the series this tier forecasts from
    Order = incoming demand + change in target stock, where
    target stock = (lead time + 1) x moving-average forecast.
    """
    n = len(incoming)
    orders = np.zeros(n)
    prev_target = (LEAD_TIME + 1) * signal[0]
    for t in range(n):
        lo = max(0, t - WINDOW + 1)
        forecast = signal[lo : t + 1].mean()
        target = (LEAD_TIME + 1) * forecast
        orders[t] = max(0.0, incoming[t] + target - prev_target)
        prev_target = target
    return orders


def run(sharing: bool) -> dict:
    demand = shopper_demand()
    series = {"Shoppers": demand}
    incoming = demand
    for tier in TIERS:
        signal = demand if sharing else incoming
        placed = order_up_to(incoming, signal)
        series[tier] = placed
        incoming = placed
    return series


def peak_swing(x: np.ndarray, base: float = 100.0) -> float:
    return float(np.max(np.abs(x - base)) / base * 100)


def main() -> None:
    results = {"no_sharing": run(False), "sharing": run(True)}

    print(f"Shoppers' peak change: {peak_swing(shopper_demand()):.1f}%\n")
    print(f"{'Tier':<10}{'No sharing':>14}{'Sharing POS':>14}")
    for tier in TIERS:
        a = peak_swing(results["no_sharing"][tier])
        b = peak_swing(results["sharing"][tier])
        print(f"{tier:<10}{a:>13.1f}%{b:>13.1f}%")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib not installed: skipping the chart.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for ax, (name, title) in zip(axes, [("no_sharing", "Each tier sees only its own orders"),
                                         ("sharing", "Every tier sees shopper demand")]):
        for label, s in results[name].items():
            ax.plot(s, label=label, linewidth=2 if label == "Shoppers" else 1.5)
        ax.set_title(title)
        ax.set_xlabel("Week")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Units ordered")
    axes[1].legend(loc="upper right")
    fig.suptitle("A 5% bump in shopper demand, four tiers upstream")
    fig.tight_layout()
    out = Path(__file__).with_name("bullwhip.png")
    fig.savefig(out, dpi=140)
    print(f"\nChart written to {out}")


if __name__ == "__main__":
    main()
