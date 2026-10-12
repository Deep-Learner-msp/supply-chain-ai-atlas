# 01. Plan: demand, inventory, S&OP

Planning decides how much will sell, how much stock to hold and where, and how to reconcile sales ambitions with what supply and production can actually do. It is owned by demand planners, inventory and supply planners, and the S&OP lead, usually inside a supply chain or operations function with finance at the table. It matters because every other stage executes against the plan: a biased forecast becomes excess stock in the warehouse, expedited freight on the road and a factory changing over too often. Plan is also where the [bullwhip effect](../../implementations/01-bullwhip-simulator) starts, because each tier forecasts the orders of the tier below instead of real demand ([Lee, Padmanabhan and Whang, 1997](https://ideas.repec.org/a/inm/ormnsc/v43y1997i4p546-558.html), *background*).

The short version: forecasting is a Prediction problem, stock targets are a Planning problem, and S&OP is a Coordination problem. AI helps most when each is treated as its own type.

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Network and stocking strategy (which locations hold which items) | Strategic | Supply chain director, network design team | Yearly, or on a major change |
| Service-level targets by segment (ABC/XYZ classes) | Strategic | Supply chain director with sales and finance | Yearly or quarterly |
| Aggregate volume plan, balancing demand with capacity (S&OP) | Tactical | S&OP lead, executive team | Monthly |
| Statistical forecast and its overrides, by item and location | Tactical | Demand planner | Weekly or monthly |
| Safety stock and reorder points | Tactical | Inventory planner | Monthly, or when lead times shift |
| Promotion and new product forecasts | Tactical | Demand planner with marketing | Per event |
| Replenishment orders and allocations | Operational | Supply planner, replenishment system | Daily or weekly |
| Short-term demand sensing (next days, from latest orders and POS) | Operational | Demand planner, automated | Daily |

## KPIs
| Metric | Definition or formula | What good looks like, and why it matters |
|---|---|---|
| WMAPE | Sum of absolute errors divided by sum of actuals, `Σ|A−F| / ΣA` | Lower is better. Weighting by volume stops slow movers dominating, which plain MAPE does |
| Forecast bias | `Σ(F−A) / ΣA` | Close to zero. Persistent bias costs more than noise, because safety stock cannot fix it |
| MASE | Mean absolute error divided by the in-sample error of a naive (or seasonal naive) forecast | Below 1 means you beat the naive method. Scale-free, so it compares items |
| Forecast value added (FVA) | Error of the naive or statistical forecast minus error after each step (overrides, consensus) | Positive at every step. Negative FVA means a meeting or an override made the forecast worse |
| Cycle service level (CSL) | Share of replenishment cycles with no stock-out | Matches the target the safety stock was sized for. Easy to compute, but says nothing about how big the shortfall was |
| Fill rate | Units shipped from stock on time divided by units ordered | Usually what customers feel. Order-line and complete-order fill rates are stricter variants |
| Inventory turns | Cost of goods sold divided by average inventory value | Higher is leaner, but only meaningful next to service level |
| Days of supply | On-hand inventory divided by average daily demand | Within the policy band per segment. Outliers point to excess or risk |
| Excess and obsolete (E&O) | Value of stock beyond a cover threshold or with no demand | Falling. It is where forecast bias ends up on the balance sheet |
| S&OP plan adherence | Actual production or supply versus the agreed plan | High. Low adherence means the plan is not believed |

## Data and systems
| Data | Typical source | Notes |
|---|---|---|
| Order and shipment history | ERP | Shipments understate demand when stock ran out (censored demand). Record lost sales or stock-outs if you can |
| Point-of-sale and retailer inventory | Retailer portals, EDI 852 (Product Activity Data) | Closer to real demand than orders; the main fix for bullwhip |
| Customer forecasts and schedules | EDI 830 (Planning Schedule), collaboration portals | Common in manufacturing; quality varies by customer |
| Promotions, prices, listings | Trade promotion and pricing systems | The largest driver of consumer goods demand spikes, and often the worst-recorded |
| Calendar, weather, events | Public calendars, weather services | Useful covariates; test whether they actually help before adding them |
| Lead times and their variability | Purchase order receipts in ERP | Use actual receipt dates, not quoted lead times |
| Capacity and constraints | MES, APS | Needed for S&OP feasibility |

Systems: ERP is the system of record. Advanced planning systems (APS) hold forecasting, inventory optimization and supply planning. MRP and DRP explode the plan into orders. Standards worth knowing: [GS1](https://www.gs1.org/standards) identifiers (GTIN for items, [GLN](https://www.gs1.org/standards/id-keys/gln) for locations), ANSI X12 and UN/EDIFACT messages, CPFR (collaborative planning, forecasting and replenishment) for sharing forecasts with trading partners, and the [ASCM SCOR model](https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/) for process and metric definitions.

## Classical methods that work
These are the baselines. An AI method that does not beat them on cost and service, on your data, is not ready.

| Method | Use it for | Reference |
|---|---|---|
| Naive and seasonal naive | The floor every forecast must clear; the denominator of MASE | [Hyndman and Athanasopoulos, *Forecasting: Principles and Practice*](https://github.com/robjhyndman/fpp3) |
| Exponential smoothing (ETS), Holt-Winters, ARIMA | Smooth and seasonal series | Same; fast implementations in [statsforecast](https://github.com/Nixtla/statsforecast) |
| Croston, SBA, TSB | Intermittent demand (spare parts, slow movers) | [Croston, 1972](https://doi.org/10.2307/3007885), *background* |
| ADI / CV² classification | Choosing a method per item: smooth, erratic, intermittent, lumpy | [Syntetos, Boylan and Croston, 2005](https://ideas.repec.org/a/pal/jorsoc/v56y2005i5d10.1057_palgrave.jors.2601841.html), *background* |
| Gradient-boosted trees over many series (LightGBM) | Retail demand with prices, promotions and calendars | [M5 results](https://doi.org/10.1016/j.ijforecast.2021.11.013): most of the top methods used LightGBM |
| Base-stock and (s, S) policies, newsvendor | Single-location stock targets | [Silver, Pyke and Thomas](https://www.routledge.com/Inventory-and-Production-Management-in-Supply-Chains/Silver-Pyke-Thomas/p/book/9781466558618) |
| Safety stock with demand and lead-time variance | Reorder points (see the worked example) | Same |
| Multi-echelon inventory optimization (stochastic-service and guaranteed-service models) | Where to hold buffers across a network | [Clark and Scarf, 1960](https://ideas.repec.org/a/inm/ormnsc/v6y1960i4p475-490.html), *background*; implemented in [stockpyl](https://github.com/LarrySnyder/stockpyl) |
| Linear and mixed-integer programming | S&OP feasibility and supply plans | [Snyder and Shen](https://www.wiley.com/en-us/Fundamentals+of+Supply+Chain+Theory%2C+2nd+Edition-p-9781119024842) |
| Forecast combination (simple averages of methods) | A cheap default worth testing against any single model | The M5 winner was an equal-weighted ensemble of LightGBM models ([M5 results](https://doi.org/10.1016/j.ijforecast.2021.11.013)) |

## What fits
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Demand forecasting | Prediction | Statistical baselines, gradient-boosted trees, time-series foundation models | Asking an LLM to write the numbers |
| Intermittent and lumpy demand | Prediction | Croston-type methods, ML combined with them, scoring on service and cost | Choosing the model on point error alone |
| Inventory targets | Planning | Stochastic inventory models, simulation, multi-echelon optimization | Hand-set "weeks of cover" rules that ignore variability |
| Policy design for unusual settings | Planning | LLM-proposed policy classes whose parameters a solver tunes and a simulator checks | LLM-chosen order quantities |
| Planner questions ("what if demand drops 10%?") | Planning + language | An LLM that translates the question into solver inputs and explains the result | An LLM that answers from its own reasoning |
| S&OP preparation and consensus | Coordination | Agents that assemble the pack, chase missing inputs, flag gaps between plans | Letting the agent commit volumes |
| Override capture and FVA | Coordination | Logging every override with its reason, then scoring it | Overrides with no audit trail |
| Partner demand sharing | Shared truth | POS sharing first; federated learning and secure aggregation when data can't move | A shared model with no local layer |

## AI in practice, 2025 to 2026
| Claim | Verdict | Evidence |
|---|---|---|
| Machine learning beats statistical methods for retail demand | **Working**, where there are many related series and good covariates | In M5 (Walmart, 42,840 series) all 50 top-performing methods were ML and significantly better than every statistical benchmark; the winner improved on the best benchmark by 22.4%, and most top methods used LightGBM ([Makridakis et al., 2022](https://doi.org/10.1016/j.ijforecast.2021.11.013)) |
| Time-series foundation models are useful zero-shot baselines | **Working**, as a baseline to beat or a fallback for new items | [Chronos-2](https://arxiv.org/abs/2510.15821), [TiRex](https://arxiv.org/abs/2505.23719), [EXAONE Demand](https://arxiv.org/abs/2609.30880) (built for demand, including intermittent and lumpy classes) |
| Foundation model intervals can be trusted out of the box | **Partly**. Better than often assumed, still check on your data | A study of five models found them better calibrated than two baselines and not systematically over- or under-confident ([Adler et al., 2025](https://arxiv.org/abs/2510.16060)). Benchmarks also have contamination traps ([2510.13654](https://arxiv.org/abs/2510.13654)) |
| The most accurate forecast gives the best service | **False for intermittent demand** | On a spare-parts panel of 38 methods, accuracy rank and order-service rank were negatively correlated (−0.555); the direction of bias mattered more ([Chin et al., 2026](https://arxiv.org/abs/2609.13840)) |
| LLMs forecast time series | **Hype** | Removing the LLM from three popular LLM forecasters did not hurt accuracy, and often improved it ([Tan et al., 2024](https://arxiv.org/abs/2406.16964), *background*) |
| LLMs can set order quantities directly | **Hype** | LLMs replicated the classic newsvendor ordering bias and amplified demand chasing, even when given the optimal formula ([Liu et al., 2025](https://arxiv.org/abs/2512.12552)). A hybrid where the LLM only elicits inputs and calls solvers cut total inventory cost by 32.1% versus GPT-4o as an end-to-end solver ([Duan et al., 2025](https://arxiv.org/abs/2601.00121)) |
| LLMs as an interface to optimization | **Working** | The OptiGuide line of work ([2307.03875](https://arxiv.org/abs/2307.03875), *background*) and [Simchi-Levi et al., 2025](https://arxiv.org/abs/2507.21502); see demo 04 |
| LLMs discovering new inventory policies | **Promising, early** | LLM-generated policy classes, with a solver tuning parameters, cut cost 30.0% versus optimized base-stock across 30 lost-sales instances; an LLM-only variant did much worse ([Yang et al., 2026](https://arxiv.org/abs/2609.08071)). See also [InvEvolve](https://arxiv.org/abs/2605.00369) |
| Deep RL for inventory control | **Promising** in lab settings with known structure | A DirectBackprop-based method was competitive with or beat benchmarks across lost-sales, perishable and dual-sourcing settings ([Maggiar et al., 2025](https://arxiv.org/abs/2507.22040)) |
| ML speeds up large planning MIPs | **Working** in industrial pilots | PROPEL reports 60% lower primal integral and 88% lower primal gap on industrial plans with millions of variables ([2504.07383](https://arxiv.org/abs/2504.07383)) |
| Federated forecasting between partners | **Pilot stage** | Evidence is mostly synthetic; [2608.21399](https://arxiv.org/abs/2608.21399) states its results are internal-consistency evidence, not real-world validation. See demo 07 |

## Worked example: safety stock under lead-time variability
*Illustrative numbers.* A distribution centre ships an item with average demand `d = 100` units/day and standard deviation `σd = 20` units/day. The supplier lead time averages `L = 10` days with standard deviation `σL = 2` days. Target cycle service level 95%, so `z = 1.645`.

The standard deviation of demand over the lead time, when both demand and lead time vary independently:

```
σLT = sqrt(L·σd² + d²·σL²) = sqrt(10·400 + 10,000·4) = sqrt(44,000) ≈ 209.8 units
SS  = z · σLT ≈ 1.645 · 209.8 ≈ 345 units
ROP = d·L + SS ≈ 1,000 + 345 = 1,345 units
```

| Scenario | σLT | Safety stock |
|---|---|---|
| Demand variance only (`σL` ignored) | 63.2 | 104 |
| Lead-time variability halved (`σL = 1`) | 118.3 | 195 |
| Both, as above (`σL = 2`) | 209.8 | 345 |

What to notice:
- Lead-time variability accounts for 40,000 of the 44,000 units² of variance. A better forecast barely moves this number; a more reliable supplier halves it.
- If you size stock on demand variance alone (104 units) when lead times really vary, the effective `z` falls to about 0.50. Cycle service drops from 95% to about 69%. With an order quantity of 700 units, fill rate drops from about 99.4% to about 94.0% (using the standard normal loss function).
- This is why Plan and [Source](02-source.md) belong together: supplier lead-time reliability is an inventory lever.

Run the full version, with simulation: [09-safety-stock](../../implementations/09-safety-stock).

## Common mistakes
- **Scoring forecasts on accuracy only.** Measure bias, and score inventory decisions on service and cost. For slow movers, error metrics can reward forecasting zero (see demo 03).
- **Training on shipments as if they were demand.** Stock-outs censor history; the model learns to forecast your past availability.
- **Ignoring lead-time variability** in safety stock (see the worked example).
- **Using quoted lead times** instead of measured receipt dates.
- **Applying one service level to every item.** Segment by value and variability.
- **Overrides without FVA tracking.** Planners and sales adjust forecasts; few companies check whether the adjustments help.
- **Comparing a new model with a weak baseline.** Always include seasonal naive, ETS and a tuned gradient-boosted model.
- **Leakage in backtests.** Promotions or prices known only after the fact, random rather than time-ordered splits, and foundation models pretrained on the test set.
- **Letting an LLM produce the plan.** It is the interface, not the engine.
- **Treating S&OP as a forecasting problem.** The hard part is agreement across sales, operations and finance.

## Run it
- [01-bullwhip-simulator](../../implementations/01-bullwhip-simulator): why sharing demand signals matters
- [03-forecast-baselines](../../implementations/03-forecast-baselines): baselines, MASE and interval coverage
- [04-llm-solver-interface](../../implementations/04-llm-solver-interface): the LLM translates, the solver plans
- [07-federated-forecasting](../../implementations/07-federated-forecasting): sharing models without sharing data, and where it breaks
- [09-safety-stock](../../implementations/09-safety-stock): safety stock under lead-time variability

## Key papers
Full list: [papers](../../papers/2025-2026.md).
| Paper | Why read it |
|---|---|
| [Chronos-2](https://arxiv.org/abs/2510.15821) | Foundation forecaster with covariates; a strong zero-shot baseline |
| [EXAONE Demand 1.0](https://arxiv.org/abs/2609.30880) | Foundation model built for demand: short histories, zeros, stock-out censoring |
| [TiRex](https://arxiv.org/abs/2505.23719) | Zero-shot forecasting across short and long horizons |
| [Are time series foundation models well-calibrated?](https://arxiv.org/abs/2510.16060) | Calibration evidence before you build safety stock on model intervals |
| [Accuracy Is Not Service](https://arxiv.org/abs/2609.13840) | 38 methods on spare parts: the most accurate forecast is not the best for service |
| [Large Language Newsvendor](https://arxiv.org/abs/2512.12552) | LLMs reproduce and amplify human ordering biases |
| [Ask, Clarify, Optimize](https://arxiv.org/abs/2601.00121) | LLM as interface to inventory solvers beats LLM as solver |
| [Automated Design of Inventory Policy with LLMs](https://arxiv.org/abs/2609.08071) | LLMs propose policy classes, a solver tunes them |
| [InvEvolve](https://arxiv.org/abs/2605.00369) | LLM-evolved white-box inventory policies with statistical safety checks |
| [Structure-Informed Deep RL for Inventory Management](https://arxiv.org/abs/2507.22040) | Deep RL that recovers known structure of optimal policies |
| [InvAgent](https://arxiv.org/abs/2407.11384) | One LLM agent per tier of a multi-echelon chain (2024, revised 2025) |
| [PROPEL](https://arxiv.org/abs/2504.07383) | ML that shrinks industrial planning MIPs |
| [LLMs for Supply Chain Decisions](https://arxiv.org/abs/2507.21502) | Simchi-Levi et al. on where LLMs speed up planning decisions |
| [Federated ensemble forecasting under volatility](https://arxiv.org/abs/2608.21399) | Why averaging dilutes rare regimes (synthetic evaluation) |
| [Deepbullwhip](https://arxiv.org/abs/2604.13478) | Open-source simulator and benchmark for multi-echelon bullwhip |

## Tools and datasets
| Resource | Use |
|---|---|
| [statsforecast](https://github.com/Nixtla/statsforecast), [neuralforecast](https://github.com/Nixtla/neuralforecast) | Statistical and neural baselines |
| [chronos-forecasting](https://github.com/amazon-science/chronos-forecasting), [timesfm](https://github.com/google-research/timesfm), [uni2ts](https://github.com/SalesforceAIResearch/uni2ts) | Foundation forecasters |
| [stockpyl](https://github.com/LarrySnyder/stockpyl) | Newsvendor, EOQ, multi-echelon (stochastic-service and guaranteed-service) models |
| [or-gym](https://github.com/hubbs5/or-gym), [SCIMAI-Gym](https://github.com/frenkowski/SCIMAI-Gym) | RL environments for inventory |
| [M5 Forecasting, Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy) | Hierarchical Walmart demand, the standard retail benchmark |
| [Favorita Grocery Sales Forecasting](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting) | Grocery demand with promotions and perishables |
| [GIFT-Eval](https://arxiv.org/abs/2410.10393) ([leaderboard](https://huggingface.co/spaces/Salesforce/GIFT-Eval)) | General benchmark for foundation forecasters, *background* |

More: [tools](../../repos/README.md), [datasets](../../datasets/README.md).

## Open problems
- Shared models average away rare shocks (a tariff change) that matter most.
- Partners won't join a shared model until the value split feels fair.
- Policy regimes with no history have nothing to train on.
- Forecast accuracy is reported; the cost of being wrong rarely is.
- **Censored demand.** Sales history hides demand lost to stock-outs. Most ML and foundation models train on it as if it were true demand, and few benchmarks record stock-outs.
- **Decision-aware evaluation.** Benchmarks such as GIFT-Eval rank point and probabilistic accuracy. There is no widely used benchmark that scores forecasters by the inventory cost and service they produce across many real datasets.
- **Explaining a plan to the S&OP meeting.** LLMs can narrate a solver's output, but checking that the narrative matches the numbers is still manual.
- **Learning from overrides.** Planners know things the data does not. Capturing why they override, and when they are right, is mostly unstudied.

See all: [open problems](../open-problems.md).

## Further reading
- Hyndman and Athanasopoulos, *Forecasting: Principles and Practice*, free online ([source](https://github.com/robjhyndman/fpp3)).
- Silver, Pyke and Thomas, [*Inventory and Production Management in Supply Chains*](https://www.routledge.com/Inventory-and-Production-Management-in-Supply-Chains/Silver-Pyke-Thomas/p/book/9781466558618), 4th edition.
- Snyder and Shen, [*Fundamentals of Supply Chain Theory*](https://www.wiley.com/en-us/Fundamentals+of+Supply+Chain+Theory%2C+2nd+Edition-p-9781119024842), 2nd edition.
- MIT OpenCourseWare, [15.762J Supply Chain Planning](https://ocw.mit.edu/courses/15-762j-supply-chain-planning-spring-2011/).
- MITx [MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM).
- [International Institute of Forecasters](https://forecasters.org/), publisher of the *International Journal of Forecasting*.
- ASCM [SCOR](https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/) and the [CPIM](https://www.ascm.org/learning-development/certifications-credentials/cpim/) certification.
