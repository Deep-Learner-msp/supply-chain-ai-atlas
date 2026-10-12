# 05. Store: warehouse, yard and dock

## Decisions
Where each item lives (slotting), which dock door and when, how to sequence the yard, how to staff shifts.

## What fits
| Sub-problem | Type | Reach for |
|---|---|---|
| Dock and appointment scheduling | Planning | Scheduling solvers, ETA-aware rescheduling |
| Slotting | Planning | Optimization on pick frequency and affinity |
| Labour planning | Prediction + planning | Forecasts feeding shift optimization |
| Yard and inventory counts | Vision | Computer vision |

## Run it
- [05-dock-scheduling](../../implementations/05-dock-scheduling)

## Key papers
Full list: [papers](../../papers/2025-2026.md).
- [SOAR: orders and robots scheduled together](https://arxiv.org/abs/2605.03842)
- [WareRover simulator](https://arxiv.org/abs/2602.13999)
- [Multi-agent pickup and delivery in constrained warehouses](https://arxiv.org/abs/2608.26939)
- [Knowledge graphs and LLMs for warehouse bottlenecks](https://arxiv.org/abs/2507.17273)

## Open problems
- Labour planning when robots take part of the work.
- Rescheduling docks in real time without creating new conflicts.
