"""
Federated demand forecasting between three retailers, and where it breaks.

Each retailer sells the same product. Weekly demand depends on price and
promotions. Each has only 30 weeks of history, so each local model is noisy.
None will share raw sales data.

Compared:
  local        : each retailer trains alone
  federated    : FedAvg; retailers share model updates, never raw data
  centralized  : everyone pools data (the upper bound nobody will agree to)
  personalized : federated model, then a few local fine-tuning steps

Part 2: retailer C hits a shock (a tariff week cluster where shoppers react
far more strongly to price). The shared model averages that away.

Run: python federated.py
"""

import numpy as np

rng = np.random.default_rng(3)
TRUE = np.array([64.0, -8.0, 25.0])  # demand at the average price, price effect, promo effect


def make(n, coef):
    price = rng.uniform(4, 10, n)
    promo = (rng.random(n) < 0.25).astype(float)
    X = np.column_stack([np.ones(n), price - 7.0, promo])  # price centred on 7
    y = X @ coef + rng.normal(0, 8, n)
    return X, y


def mse(w, X, y): return float(np.mean((X @ w - y) ** 2))


def gd(w, X, y, steps, lr=0.05):
    for _ in range(steps):
        w = w - lr * 2 * X.T @ (X @ w - y) / len(y)
    return w


def fit_ls(X, y): return np.linalg.lstsq(X, y, rcond=None)[0]


def fedavg(clients, rounds=300, local_steps=5):
    w = np.zeros(3)
    sizes = np.array([len(y) for _, y in clients], dtype=float)
    for _ in range(rounds):
        updates = [gd(w.copy(), X, y, local_steps) for X, y in clients]
        w = np.average(updates, axis=0, weights=sizes)
    return w


def evaluate(title, coefs):
    train = [make(30, c) for c in coefs]
    test = [make(200, c) for c in coefs]
    w_local = [fit_ls(X, y) for X, y in train]
    w_fed = fedavg(train)
    w_cen = fit_ls(np.vstack([X for X, _ in train]), np.concatenate([y for _, y in train]))
    w_per = [gd(w_fed.copy(), X, y, 15) for X, y in train]
    print(f"\n{title}  (test error, MSE: lower is better)")
    print(f"{'Retailer':<10}{'Local':>9}{'Federated':>11}{'Central':>9}{'Personal':>10}")
    for i, (Xt, yt) in enumerate(test):
        print(f"{'ABC'[i]:<10}{mse(w_local[i], Xt, yt):>9.0f}{mse(w_fed, Xt, yt):>11.0f}"
              f"{mse(w_cen, Xt, yt):>9.0f}{mse(w_per[i], Xt, yt):>10.0f}")


def main():
    evaluate("Part 1: same market", [TRUE, TRUE, TRUE])
    shocked = TRUE.copy()
    shocked[1] = -16.0  # retailer C's shoppers react twice as strongly to price
    evaluate("Part 2: retailer C in a price shock", [TRUE, TRUE, shocked])
    print("\nShared models help when partners look alike, and blur the partner who is different."
          "\nThat partner is often the one seeing the shock first.")


if __name__ == "__main__":
    main()
