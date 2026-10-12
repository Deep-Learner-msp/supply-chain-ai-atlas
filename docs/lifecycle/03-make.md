# 03. Make: production and scheduling

## Decisions
What to produce, on which line, in which order, and when to change over.

## What fits
| Sub-problem | Type | Reach for |
|---|---|---|
| Production scheduling | Planning | Constraint programming, MILP, learned heuristics |
| Explaining a schedule | Planning + language | LLM over solver output |
| Predictive maintenance | Prediction | Sensor models, anomaly detection |
| Quality inspection | Documents/vision | Computer vision |

## Key papers
Full list: [papers](../../papers/2025-2026.md).
- [Starjob: LLM job-shop scheduling](https://arxiv.org/abs/2503.01877)
- [HeuriGym](https://arxiv.org/abs/2506.07972)
- [CO-Bench](https://arxiv.org/abs/2504.04310)
- [OptiRepair: agents that repair optimization models](https://arxiv.org/abs/2602.19439)
- [Evaluating ML-based combinatorial solvers](https://arxiv.org/abs/2505.16952)

## Open problems
- LLM-written heuristics look good on benchmarks; plant constraints are messier.
- Verifying that an LLM-formulated model matches the real plant.
