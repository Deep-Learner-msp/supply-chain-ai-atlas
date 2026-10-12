# 04. Move: transport and routing

## Decisions
Which mode and carrier, which route, when to tender, how to recover a late load.

## Data
Tenders and EDI messages, telematics and GPS, rates, lanes, appointment times, carrier performance.

## What fits
| Sub-problem | Type | Reach for |
|---|---|---|
| Vehicle routing | Planning | Routing solvers (OR-Tools, PyVRP), learning-to-optimize methods |
| ETA prediction | Prediction | Gradient-boosted trees on lane and dwell features |
| Carrier follow-up, rebooking | Coordination | LLM agents with guardrails |
| Freight documents | Documents | Document AI plus rules |

## Context
ATRI's research found truck drivers detained at 39.3% of stops in 2023. Most of that time is coordination, not prediction.

## Run it
- [04-llm-solver-interface](../../implementations/04-llm-solver-interface)
- [06-agent-with-guardrails](../../implementations/06-agent-with-guardrails)

## Key papers
Full list: [papers](../../papers/2025-2026.md).
- [RRNCO: real-world neural routing](https://arxiv.org/abs/2503.16159)
- [Learning to segment for VRPs](https://arxiv.org/abs/2507.01037)
- [Constraint handling in neural routing solvers](https://arxiv.org/abs/2602.16012)
- [Neural cluster first, route second](https://arxiv.org/abs/2605.09301)
- [Cross-problem routing via federated learning](https://arxiv.org/abs/2604.10652)

## Open problems
- Calibrated ETAs: accuracy is reported, the value of the error bar rarely is.
- Driverless trucks arriving at yards and gates designed for a driver to talk to.
- Learned routing methods at real fleet scale with real constraints.
