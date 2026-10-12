# 01. Plan: demand, inventory, S&OP

## Decisions
How much will sell, by product and location. How much stock to hold and where. How to balance sales targets with production and supply limits (S&OP).

## Data
Point-of-sale and order history, promotions, prices, weather, events, lead times, supplier capacity.

## What fits
| Sub-problem | Type | Reach for |
|---|---|---|
| Demand forecasting | Prediction | Statistical baselines, gradient-boosted trees, time-series foundation models |
| Inventory targets | Planning | Stochastic inventory models, simulation, multi-echelon optimization |
| Planner questions ("what if demand drops 10%?") | Planning + language | An LLM that translates the question into solver inputs and explains the result |
| Partner demand sharing | Shared truth | Federated learning, secure aggregation |

## Run it
- [01-bullwhip-simulator](../../implementations/01-bullwhip-simulator)
- [03-forecast-baselines](../../implementations/03-forecast-baselines)
- [04-llm-solver-interface](../../implementations/04-llm-solver-interface)
- [07-federated-forecasting](../../implementations/07-federated-forecasting)

## Key papers
Full list: [papers](../../papers/2025-2026.md).
- [Chronos-2](https://arxiv.org/abs/2510.15821)
- [EXAONE Demand 1.0](https://arxiv.org/abs/2609.30880)
- [TiRex](https://arxiv.org/abs/2505.23719)
- [Are time series foundation models well-calibrated?](https://arxiv.org/abs/2510.16060)
- [InvAgent: multi-agent inventory management](https://arxiv.org/abs/2407.11384)
- [Ask, Clarify, Optimize](https://arxiv.org/abs/2601.00121)
- [PROPEL](https://arxiv.org/abs/2504.07383)
- [LLMs for Supply Chain Decisions](https://arxiv.org/abs/2507.21502)
- [Federated ensemble forecasting under volatility](https://arxiv.org/abs/2608.21399)

## Open problems
- Shared models average away rare shocks (a tariff change) that matter most.
- Partners won't join a shared model until the value split feels fair.
- Policy regimes with no history have nothing to train on.
- Forecast accuracy is reported; the cost of being wrong rarely is.
