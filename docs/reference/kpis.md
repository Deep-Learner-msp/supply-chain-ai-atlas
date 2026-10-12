# KPI dictionary

The numbers supply chains run on, stage by stage. Each entry gives the standard formula and the ways it gets gamed or misread.

Conventions used below:
- `y` is the actual value, `ŷ` the forecast, `e = y - ŷ` the error, `n` the number of periods or items.
- `Σ` sums over the items and periods being scored.
- "Count" metrics (orders, lines, loads) and "value" metrics (units, money) give different answers. Always say which one you report.

Where an industry body defines a metric, the entry says so. Definitions vary by company and contract, so write yours down before you compare across partners.

Sources used throughout:
- ASCM [SCOR Digital Standard](https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/): the reference process and metrics model for supply chains, including perfect order fulfilment and cash-to-cash cycle time.
- Hyndman and Athanasopoulos, [Forecasting: Principles and Practice, 3rd ed.](https://otexts.com/fpp3/) (FPP3): [point accuracy](https://otexts.com/fpp3/accuracy.html) and [distribution accuracy](https://otexts.com/fpp3/distaccuracy.html).
- Hyndman and Koehler (2006), [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001), International Journal of Forecasting: the paper that introduced MASE.

## Plan: forecasting and demand

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| MAE | `mean(abs(e))` | In units of the data, so it cannot be averaged across items with different scales. Minimizing MAE gives median forecasts (FPP3). |
| RMSE | `sqrt(mean(e²))` | Punishes large misses more than MAE. Minimizing it gives mean forecasts (FPP3). Scale dependent, like MAE. |
| MAPE | `100 × mean(abs(e / y))` | Undefined when any `y = 0` and explodes when `y` is near zero. Penalizes over-forecasts more heavily than under-forecasts (FPP3). Unusable on intermittent demand. |
| sMAPE | `mean(200 × abs(y - ŷ) / (y + ŷ))` | Not actually symmetric and unstable near zero. Hyndman and Koehler recommend against it. |
| WAPE (also called MAD/mean ratio) | `Σ abs(e) / Σ abs(y)` | Total absolute error over total volume. Survives zeros in single periods. Dominated by fast movers: a good WAPE can hide terrible slow-mover forecasts. |
| MASE | `mean(abs(e_j)) / [ (1/(T-m)) × Σ_{t=m+1..T} abs(y_t - y_{t-m}) ]` | Error scaled by the in-sample MAE of a naive (`m = 1`) or seasonal naive (`m` = season length) forecast. Below 1 beats that naive method on the training data. Scale free, so it averages across SKUs. Defined by Hyndman and Koehler (2006). |
| RMSSE | `sqrt(mean(q_j²))`, where `q_j` is the error scaled by the in-sample mean squared naive error | Squared version of MASE. Used in the M5 competition. |
| Forecast bias | `Σ (ŷ - y) / Σ y` | Positive means over-forecasting (excess stock), negative means under-forecasting (stock-outs). Sign conventions differ between tools: state yours. |
| Tracking signal | `Σ e / MAE` over a rolling window | Flags persistent bias. A common alarm band is about ±4, but tune it to your volatility. |
| Pinball (quantile) loss | for quantile `τ` and forecast `q`: `τ × (y - q)` if `y ≥ q`, else `(1 - τ) × (q - y)` | Scores one quantile of a probabilistic forecast. FPP3 calls it the quantile score and multiplies by 2. Averaging it over all quantiles approximates CRPS. |
| Interval coverage | share of actuals inside the stated interval `[l, u]` | An 80% interval should contain about 80% of outcomes. Report it next to every accuracy number. See [demo 03](../../implementations/03-forecast-baselines). |
| Winkler score | width `(u - l)`, plus `(2/α) × (l - y)` if `y < l`, plus `(2/α) × (y - u)` if `y > u` | Rewards narrow intervals and penalizes misses. Lower is better. Defined in FPP3. |
| CRPS | integral of squared difference between forecast CDF and the step function at `y` | Scores the whole forecast distribution. Reduces to MAE for a point forecast. |
| Forecast value added (FVA) | `error(naive) - error(process step)` | Measures whether each step (statistical model, planner override, consensus) improved on the step before. Negative FVA for overrides is common. |
| Skill score | `(score_benchmark - score_method) / score_benchmark` | Proportional improvement over a baseline (FPP3). Report against seasonal naive at minimum. |

See [01-plan](../lifecycle/01-plan.md).

## Source: suppliers and procurement

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Supplier lead time | `receipt date - purchase order date` | Report mean and standard deviation, not only the mean. Safety stock depends on both. |
| Lead time variability | standard deviation (or coefficient of variation, `σ / μ`) of lead time | A supplier with a longer but stable lead time can need less safety stock than a faster, erratic one. |
| Supplier OTIF | `PO lines received on time and in full / PO lines due` | Fix the window (for example, -2 to 0 days) and the quantity tolerance before scoring. |
| Supplier defect rate (PPM) | `defective units / units received × 1,000,000` | Count rejects found later in production too, not only at receiving inspection. |
| Purchase price variance (PPV) | `(actual price - standard price) × quantity` | Rewards buying cheaper even when it costs more downstream (freight, quality, lead time). Pair it with total landed cost. |
| Spend under contract | `spend on contracted terms / total addressable spend` | Depends on how spend is classified. AI spend classifiers change this number. |

See [02-source](../lifecycle/02-source.md).

## Make: production

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| OEE | `Availability × Performance × Quality` | Availability = `run time / planned production time`. Performance = `(ideal cycle time × total count) / run time`. Quality = `good count / total count`. "World class" targets assume a definition of planned time that many plants quietly change. |
| Schedule adherence (attainment) | `Σ min(actual_i, planned_i) / Σ planned_i` | Capping at plan stops over-production of one item from hiding a shortfall in another. Measure against the frozen schedule, not the last re-plan. |
| First pass yield | `units good first time / units started` | Excludes rework. Rolled throughput yield multiplies first pass yield across steps. |
| Changeover time | `time from last good unit of A to first good unit of B` | Drives batch size and sequence in scheduling models, such as the CP-SAT model in [demo 05](../../implementations/05-dock-scheduling). |
| Capacity utilization | `actual output / available capacity` | High utilization makes queues explode (Kingman). Near 100% is a warning sign, not a target. |

See [03-make](../lifecycle/03-make.md).

## Move: transport

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Cost per mile | `total transport cost / total miles` | State whether miles are loaded only or loaded plus empty, and whether fuel surcharge and accessorials are included. |
| Empty miles | `empty miles / total miles` | Also called deadhead. A network metric: one shipper's lanes rarely tell you the carrier's true empty share. |
| Tender acceptance rate | `tenders accepted / tenders offered` | First tender acceptance counts only the primary carrier in the routing guide. Low acceptance pushes freight to the spot market. Based on EDI 204 and 990 messages (see [data standards](data-standards.md)). |
| On-time pickup / delivery | `stops within the appointment window / total stops` | Define the window and whether carrier-caused and facility-caused misses are split. |
| Dwell time | `departure time - arrival time` at a facility | Needs reliable arrival and departure events (geofence or EDI 214). Report the distribution, not only the mean. |
| Detention | billable time = `max(0, dwell - free time)` | Free time is often two hours but is set by contract. ATRI found drivers detained at 39.3% of stops in 2023 ([04-move](../lifecycle/04-move.md)). |
| ETA accuracy | `mean(abs(predicted arrival - actual arrival))` at a fixed horizon | Score at fixed horizons (24h, 4h, 1h out), never averaged across all pings. Also report the share within a window (for example, ±30 minutes) and interval coverage. |
| Transit time variability | standard deviation or P90 minus P50 of transit time per lane | Drives safety stock at the destination as much as the mean transit does. |
| Cost per hundredweight (CWT) | `freight cost / (shipment weight in lb / 100)` | LTL pricing unit. Compare only within the same freight class. |
| Trailer / asset utilization | `loaded hours (or cube used) / available hours (or cube)` | Weight-limited and cube-limited freight need different measures. |

See [04-move](../lifecycle/04-move.md).

## Store: warehouse and yard

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Dock-to-stock time | `put-away confirmed time - receipt at dock time` | Stock is not available to sell until put away. Long dock-to-stock looks like a supplier delay to the planner. |
| Pick rate | `lines (or units) picked / labour hours` | Lines and units give very different numbers. Compare only like-for-like order profiles. |
| Picking accuracy | `orders picked without error / orders picked` | Errors found by the customer count. Errors caught at pack-out are a cost but not a customer failure. |
| Inventory record accuracy | `locations (or SKUs) where abs(system - counted) ≤ tolerance / locations counted` | Count-based and value-based accuracy differ. Planning and AI models trust the system number, so this metric caps their quality. |
| Inventory turns | `cost of goods sold / average inventory at cost` | Use cost, not retail value, in both terms. Average over the period, not the year-end balance. |
| Days of supply | `on-hand inventory / average daily demand` | Forward-looking version uses forecast demand. The financial version (days inventory outstanding) is in the cross-cutting table. |
| Storage utilization | `occupied locations (or cube) / total` | Above roughly 85 to 90%, travel time and re-handling rise sharply. |
| Shrink | `(book inventory - physical inventory) / book inventory` | Mixes theft, damage and record errors. Split them before modelling. |
| Yard dwell | `gate-out time - gate-in time` per trailer | Ties directly to detention. See [demo 05](../../implementations/05-dock-scheduling). |

See [05-store](../lifecycle/05-store.md).

## Deliver: customer service

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Fill rate (unit, type 2 or β service) | `units shipped from stock on first attempt / units ordered` | Line fill rate and order fill rate are stricter versions. Always say which. |
| Cycle service level (type 1 or α service) | `replenishment cycles with no stock-out / total cycles` | Probability of not running out in a cycle. Not the same as fill rate: a 95% cycle service level can give a fill rate above 99%. Textbook safety stock formulas target this one. |
| OTIF | `orders delivered on time and in full / total orders` | Retailers define the window and "in full" differently and fine against their own definition. Score yourself the way your biggest customer scores you. |
| Perfect order | `orders on time, complete, damage free and with correct documents / total orders` | SCOR's top reliability metric (perfect order fulfilment). Multiplying the component rates is only an approximation: it assumes failures are independent. Count orders, not components. |
| First-attempt delivery rate | `deliveries completed at first attempt / deliveries attempted` | Key last-mile cost driver. Failed attempts double the stop cost and raise WISMO contacts. |
| Order cycle time | `delivery time - order placement time` | Report the distribution. SCOR calls the end-to-end version order fulfilment cycle time. |
| Cost per stop / per delivery | `total delivery cost / stops (or deliveries)` | Varies with drop density. Compare per route type. |
| WISMO contact rate | `"where is my order" contacts / orders` | A visibility metric, not only a service metric. Proactive ETA updates move it. |

See [06-deliver](../lifecycle/06-deliver.md).

## Return: reverse logistics

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Return rate | `units returned / units sold` | Returns lag sales, so a same-period ratio swings with seasonality. Use cohorts: returns from units sold in period `t`. |
| Recovery rate | `net value recovered from returns / original cost of returned goods` | Net of processing, transport and refurbishment cost. Recovering value on paper while spending more to process it is common. |
| Return processing time | `disposition complete time - return received time` | Value decays while goods wait, fastest for fashion and electronics. |
| Disposition mix | share of returns restocked, refurbished, liquidated, recycled, destroyed | Where AI grading and routing models earn their keep. |
| Return reason accuracy | `returns where stated reason matches inspected reason / returns inspected` | Customer-stated reasons are noisy labels. Do not train on them without checking. |

See [07-return](../lifecycle/07-return.md).

## Cross-cutting: financial, risk, emissions

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Cash-to-cash cycle time | `DIO + DSO - DPO` | SCOR asset management metric. DIO = `average inventory / COGS × 365`. DSO = `accounts receivable / revenue × 365`. DPO = `accounts payable / COGS × 365` (some use purchases instead of COGS). Stretching DPO improves it on paper and can push suppliers into risk. |
| Inventory carrying cost | `average inventory value × carrying cost rate` | The rate (capital, storage, insurance, obsolescence) is an assumption, often 15 to 30% a year. State it. |
| Total landed cost | `price + freight + duties and taxes + insurance + handling` | The right comparison for sourcing decisions, not unit price. |
| Cost to serve | all costs to serve one customer or channel `/ revenue or volume` | Needs activity-based allocation. Rarely the same as the finance view. |
| Time to recover (TTR) | time for a node to return to full function after disruption | Pair with time to survive (TTS), how long the network can meet demand without that node. Simchi-Levi's resilience framing. |
| Emissions intensity | `t CO2e / tonne-km` (transport) or `kg CO2e / unit shipped` | Follow [ISO 14083](https://www.iso.org/standard/78864.html) and the [GLEC Framework](https://smartfreightcentre.org/news/13311209). State the boundary: well-to-wheel or tank-to-wheel, and whether hub emissions are included. |
| Primary data share | `Scope 3 emissions based on supplier primary data / total Scope 3` | Shows how much of the footprint is measured rather than estimated. Only 4% of companies use primary supplier data ([08-cross-cutting](../lifecycle/08-cross-cutting.md)). |

See [data standards](data-standards.md) for the emissions accounting standards.

## AI system metrics

The model metrics above are necessary but not enough. These score the AI system as it runs.

| Metric | Formula | Notes and pitfalls |
|---|---|---|
| Calibration error | `abs(nominal coverage - observed coverage)` across interval levels | The gap between "80% interval" and how often reality lands inside it. |
| Safe success rate | `tasks reaching the goal with zero policy violations / tasks` | The ranking metric in [SCX-Bench](../../benchmark/README.md). Plain success rate rewards shortcuts. |
| Autonomous resolution rate | `cases closed without human edit / cases handled` | Report next to the error rate on the closed cases. |
| Human override rate | `recommendations changed or rejected by a planner / recommendations made` | High override rate means low trust or a wrong objective. Track the reason codes. |
| Optimality gap | `(best solution found - best bound) / best solution found` | Reported by MILP and CP solvers. A plan with a 20% gap is not "optimal". |
| Plan stability | `assignments changed / assignments in previous plan` | Re-plans that move everything are not followed. See [demo 05](../../implementations/05-dock-scheduling). |

## Metrics AI teams get wrong

| Mistake | Why it misleads | Do this instead |
|---|---|---|
| MAPE on lumpy or intermittent demand | Zero-demand periods make it undefined or infinite; tools then drop them silently | Use MASE or WAPE, and score slow movers on stock-out and holding cost ([demo 03](../../implementations/03-forecast-baselines)) |
| Accuracy without calibration | A model with the lowest error can still give intervals that cover 69% instead of 80%; safety stock built on them is too thin | Report interval coverage or pinball loss next to every point metric |
| Averaging MAPE across SKUs | One tiny SKU with a 900% error dominates the average | Use volume-weighted WAPE or scale-free MASE |
| Scoring at the wrong lag | One-week-ahead accuracy looks great; the decision was made eight weeks out at the supplier lead time | Score at the lag the decision is made |
| Reporting accuracy with no bias | Absolute error hides a model that always over-forecasts | Report bias separately, with its sign convention |
| Beating a weak baseline | "30% better" than a moving average is not news | Always include seasonal naive; report a skill score |
| Backtesting on revised history | Using cleaned or restated demand that was not known at forecast time leaks the future | Back-test on data as it was at each forecast date |
| ETA accuracy averaged over all pings | Most pings are minutes from arrival, where everyone is accurate | Score at fixed horizons |
| Fill rate and cycle service level used interchangeably | They answer different questions and differ by several points | Name the service measure in the safety stock policy |
| OTIF compared across companies | Every retailer defines the window and "in full" differently | Compare only under one written definition |
| Agent success rate without violations | An agent that refunds money to close a ticket "succeeded" | Score safe success ([SCX-Bench](../../benchmark/README.md)) |
| "Optimal" plan with no gap or stability | A solver stopped early or a plan that moves every truck | Report the optimality gap and plan stability |
