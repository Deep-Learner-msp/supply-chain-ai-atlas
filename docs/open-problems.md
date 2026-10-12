# Open problems

The research agenda this repo tracks. Each links to the lifecycle page where it lives.

| # | Problem | Stage |
|---|---|---|
| 1 | Shared demand models wash out rare shocks | [Plan](lifecycle/01-plan.md) |
| 2 | Fair value splits for federated models between partners | [Plan](lifecycle/01-plan.md), [Cross-cutting](lifecycle/08-cross-cutting.md) |
| 3 | Forecasting through policy regimes with no history | [Plan](lifecycle/01-plan.md) |
| 4 | Visibility past tier-1 suppliers | [Source](lifecycle/02-source.md) |
| 5 | Verifying LLM-formulated optimization models | [Make](lifecycle/03-make.md) |
| 6 | Calibrated ETAs and the value of the error bar | [Move](lifecycle/04-move.md) |
| 7 | Yards and gates for driverless trucks | [Move](lifecycle/04-move.md) |
| 8 | Labour planning with robots | [Store](lifecycle/05-store.md) |
| 9 | Auditable model-filled Scope 3 numbers | [Cross-cutting](lifecycle/08-cross-cutting.md) |
| 10 | A public benchmark for supply chain agents | All |
| 11 | Scoring forecasts by the cost of being wrong | [Plan](lifecycle/01-plan.md) |
| 12 | One supplier data request instead of fifty | [Source](lifecycle/02-source.md), [Cross-cutting](lifecycle/08-cross-cutting.md) |
| 13 | LLM-written heuristics on real plant constraints | [Make](lifecycle/03-make.md) |
| 14 | Re-planning that people trust: stable vs optimal | [Store](lifecycle/05-store.md), [Make](lifecycle/03-make.md) |
| 15 | Who pays for a missed delivery promise | [Deliver](lifecycle/06-deliver.md) |
| 16 | Forecasting returns and grading them at first touch | [Return](lifecycle/07-return.md) |
| 17 | Agents that read outside parties' messages safely | [Deliver](lifecycle/06-deliver.md), [Move](lifecycle/04-move.md), All |
| 18 | Allocating one factory's emissions across many customers | [Cross-cutting](lifecycle/08-cross-cutting.md) |

Working on one? Open an issue so others can find you.

## Why each one is open

**1. Shared demand models wash out rare shocks.** Pooling data across partners improves the average case. The partner who sees a shock first looks like an outlier, so averaging blurs exactly the signal that matters. In [demo 07](../implementations/07-federated-forecasting) the shocked retailer's error doubles under the shared model. Personalisation helps; nobody has shown how to detect, early and reliably, that one partner has entered a new regime. Start with [Federated Ensemble Forecasting Under Supply-Chain Market Volatility](https://arxiv.org/abs/2608.21399).

**2. Fair value splits for federated models.** A retailer with clean, large data gains less from a shared model than a small one, and may be helping a competitor. Contribution measures exist in the federated learning literature, but there is no accepted way to price a partner's contribution in a supply chain contract. Until there is, partners do not join.

**3. Forecasting through policy regimes with no history.** A new tariff, a sanction or a sudden regulatory change has no training data. Foundation models and scenario methods help, but there is no standard way to evaluate a forecast for a regime that has not happened yet. Scenario-based stress tests ([demo 10](../implementations/10-dual-sourcing) does this for sourcing) may be the honest substitute.

**4. Visibility past tier-1 suppliers.** Most firms know their direct suppliers and little beyond. Building the map from documents, news and trade data is costly, and the map goes stale. Agentic knowledge graph construction, such as [Helicase](https://arxiv.org/abs/2605.26835), is promising. Open questions: how to measure the map's accuracy and how to keep it current.

**5. Verifying LLM-formulated optimization models.** An LLM can write a model that solves to optimality and is still the wrong model. Checks that compare a formulation to the real plant, short of a human expert reading it, are immature. [OptiRepair](https://arxiv.org/abs/2602.19439) shows one route: solver-verified repairs plus domain rationality checks.

**6. Calibrated ETAs and the value of the error bar.** ETA accuracy is widely reported; whether its window keeps its promise is not. [Demo 12](../implementations/12-eta-calibration) shows Gaussian windows letting 6 times the promised share of trucks arrive late, and conformal intervals fixing coverage on average but not per segment. Open: calibrating per lane and carrier with little data, and putting a money value on a tighter honest window.

**7. Yards and gates for driverless trucks.** Gate check-in, door assignment and paperwork assume a driver to talk to. An autonomous truck needs the yard to tell it where to go and to accept documents without a person. This is a coordination and standards problem as much as a perception one, and little published work addresses it.

**8. Labour planning with robots.** When robots take part of the picking, labour demand depends on robot schedules, not just order volume. Joint planning of orders and robots exists ([SOAR](https://arxiv.org/abs/2605.03842)); joint planning of robots and people, with shift rules, is mostly open.

**9. Auditable model-filled Scope 3 numbers.** Most Scope 3 figures are estimates. [Demo 08](../implementations/08-scope3-uncertainty) shows that one estimated supplier can drive most of the uncertainty. Open: what evidence an auditor needs to accept a modelled number, and how to report its range. [Scope3Trace](https://arxiv.org/abs/2607.17122) works on evidence-based extraction from reports.

**10. A public benchmark for supply chain agents.** General agent benchmarks such as [τ-bench](https://arxiv.org/abs/2406.12045) score tool use and policy following in retail and airline settings. Supply chain cases add multiple outside parties, long delays and money. [SCX-Bench](../benchmark) is a start; open needs are realistic messy messages, multi-party cases and a public leaderboard of LLM agents.

**11. Scoring forecasts by the cost of being wrong.** Forecast competitions score error. Businesses pay for stock-outs, write-offs and expedites. On slow movers, error metrics can reward forecasting zero ([demo 03](../implementations/03-forecast-baselines)). Open: cost-aware metrics that are still comparable across companies, and model training that targets them.

**12. One supplier data request instead of fifty.** Small suppliers get a different questionnaire from every customer for emissions, risk and compliance. Standards such as WBCSD PACT help for product footprints ([data standards](reference/data-standards.md)). Open: agents and formats that let a supplier answer once and share many times, with consent and without leaking data between customers.

**13. LLM-written heuristics on real plant constraints.** Benchmarks such as [HeuriGym](https://arxiv.org/abs/2506.07972) and [CO-Bench](https://arxiv.org/abs/2504.04310) test LLM-written heuristics on well-defined problems against human-designed algorithms, and HeuriGym still finds clear limits in tool use, planning and adaptive reasoning. Real plants have changeover rules, crew limits and unwritten exceptions ([demo 11](../implementations/11-changeover-scheduling) has a small version). Open: whether these heuristics survive the move from benchmark to plant, and how to test that without a live line.

**14. Re-planning that people trust.** [Demo 05](../implementations/05-dock-scheduling) shows the optimal re-plan moving 7 trucks and the stable one moving 1. Every real scheduler trades optimality against churn, but there is no standard way to measure the cost of churn or to choose the trade-off. Planner trust research ([deploying AI](playbooks/deploying-ai.md#4-change-management-with-planners-and-floor-teams)) suggests stability matters more than the last few percent.

**15. Who pays for a missed delivery promise.** Faster promises sell more and miss more. The cost of a miss lands on customer service, the carrier or the customer, rarely on the team that set the promise. Open: promise policies that use calibrated ETA ranges and price the miss, and evidence of how customers respond to an honest range.

**16. Forecasting returns and grading them at first touch.** Returns are rarely forecast, so reverse capacity is planned last. [Demo 14](../implementations/14-returns-disposition) shows that deciding disposition at first touch beats shipping everything back, and that the remaining gap is the value of better grading. Open: consistent condition grading from photos, and returns forecasts good enough to plan reverse capacity.

**17. Agents that read outside parties' messages safely.** Supply chain agents read emails, PDFs and portal notes from carriers, suppliers and customers, none of whom you control. Indirect prompt injection ([Greshake et al. 2023](https://arxiv.org/abs/2302.12173); [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)) turns that data into instructions. Gateway design reduces the risk ([agent architecture](playbooks/agent-architecture.md)); no defence is complete, and there is no supply chain injection test suite. [AgentDojo](https://arxiv.org/abs/2406.13352) is the general starting point.

**18. Allocating one factory's emissions across many customers.** A supplier serving dozens of customers must split its emissions among them. Mass, revenue and machine-hour allocations give different answers, and each customer's report depends on the choice. Open: allocation methods that are fair, auditable and exchangeable through standards such as PACT.
