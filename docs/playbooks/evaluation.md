# Playbook: evaluating supply chain AI

How to tell whether a forecast, a solver, an agent or a document model is good enough to trust with real freight, stock and money.

Three rules apply to every technology on this page:

1. **Beat a simple baseline first.** Seasonal naive for forecasts, the current planner's plan or a greedy rule for optimization, the rule-based reference for agents, "every document goes to a human" for document AI.
2. **Score the decision, not just the prediction.** A forecast is good if the stock it drives is right. A plan is good if the floor can run it.
3. **Offline results earn an online test, nothing more.** Backtests and benchmarks decide what goes into shadow mode. Only shadow mode and controlled live tests decide what goes into production.

## At a glance

| Technology | Question | Primary metrics | Baseline | Demo |
|---|---|---|---|---|
| Forecasting | Is the number right, and is the error bar honest? | MASE, bias, interval coverage, quantile loss, cost of the stock it drives | Seasonal naive | [03](../../implementations/03-forecast-baselines), [09](../../implementations/09-safety-stock), [12](../../implementations/12-eta-calibration) |
| Optimization | Is the plan good, feasible and stable? | Optimality gap, solve time, plan churn, feasibility on real constraints, tail cost | Current plan or a greedy rule | [05](../../implementations/05-dock-scheduling), [10](../../implementations/10-dual-sourcing), [11](../../implementations/11-changeover-scheduling) |
| Agents | Did it reach the goal without breaking policy? | Safe success, violations, pass^k, cost per case, escalation rate | Rule-based reference agent | [06](../../implementations/06-agent-with-guardrails), [SCX-Bench](../../benchmark) |
| Document AI | Are the fields right, and do the bad ones get caught? | Field precision and recall, straight-through rate, residual error rate, false alarms | All documents keyed by hand | [13](../../implementations/13-document-validation) |
| Sustainability data | How wide is the honest range? | Interval width, contribution to variance | Single spend-based number | [08](../../implementations/08-scope3-uncertainty) |

Formulas for the metrics are in the [KPI dictionary](../reference/kpis.md).

## Forecasting

### Backtest the way you will forecast

Use rolling-origin evaluation (time series cross-validation): fit on data up to week t, forecast the next h weeks, move t forward, repeat. Never shuffle time. See FPP3, [Time series cross-validation](https://otexts.com/fpp3/tscv.html).

| Do | Why |
|---|---|
| Forecast at the horizon the decision uses | Replenishment with a 3-week lead time needs the week 3 forecast scored, not week 1 |
| Use only data available at forecast time | Promotions planned later, revised sales and late returns leak the future |
| Score many origins, not one holdout | One holdout window can be lucky |
| Check foundation models for test leakage | Public benchmarks may be in their training data; see [information leakage in TSFM evaluation](https://arxiv.org/abs/2510.13654) |

### Point accuracy

| Metric | Use it for | Watch out |
|---|---|---|
| MASE | Comparing across SKUs and against naive. Below 1 beats the in-sample one-step naive (seasonal naive for seasonal data) ([FPP3](https://otexts.com/fpp3/accuracy.html), [Hyndman and Koehler 2006](https://doi.org/10.1016/j.ijforecast.2006.03.001)) | On intermittent demand, error metrics can reward forecasting zero ([demo 03](../../implementations/03-forecast-baselines)) |
| Bias | Systematic over- or under-forecasting | A low MASE can hide a steady bias that drives stock the wrong way |
| WAPE | Volume-weighted reporting to the business | Fast movers dominate; slow movers disappear |

Avoid MAPE on anything with zeros or small volumes. The [KPI dictionary](../reference/kpis.md) explains why.

### Probabilistic accuracy

Safety stock, ETA windows and promise dates are set from the error bar, so score the error bar.

| Metric | Meaning | Source |
|---|---|---|
| Interval coverage | Share of actuals inside the 80% (or 95%) interval. It should be close to 80% | [FPP3, prediction intervals](https://otexts.com/fpp3/prediction-intervals.html) |
| One-sided coverage | Share of actuals above the upper bound. For ETAs this is the share of late trucks | [Demo 12](../../implementations/12-eta-calibration) |
| Quantile (pinball) loss, CRPS | Scores the whole distribution, not just one interval | [FPP3, distributional accuracy](https://otexts.com/fpp3/distaccuracy.html) |

Accuracy and calibration are different. In demo 03 the most accurate model covers 69% with its 80% intervals. In demo 12 a Gaussian ETA window promises 99% and lets 3.2% of trucks arrive late; a split conformal window on the same model hits the target. A 2025 study of five time-series foundation models found them better calibrated than the baselines it tested ([Beyond Accuracy](https://arxiv.org/abs/2510.16060)). That is encouraging, and still not a reason to skip the check on your own data.

### Business-cost metrics

| Metric | What it tells you | Demo |
|---|---|---|
| Achieved service level vs target | Whether the stock policy built on the forecast keeps its promise | [09](../../implementations/09-safety-stock): a demand-only formula targets 95% and achieves 69% |
| Stock-out cost plus holding cost | The money a forecast error actually costs | [03](../../implementations/03-forecast-baselines) for slow movers |
| Late share at the promised window | Customer-facing cost of an ETA | [12](../../implementations/12-eta-calibration) |

Pick the model on the business metric. Report the accuracy metric so others can compare.

For a public reference point, the M5 competition scored 42,840 hierarchical Walmart series with a weighted, scaled error and published what beat simple benchmarks ([Makridakis et al. 2022](https://doi.org/10.1016/j.ijforecast.2021.11.013)). For general forecasting models, [GIFT-Eval](https://arxiv.org/abs/2410.10393) is a cross-domain benchmark. Neither replaces a backtest on your own series.

## Optimization

| Metric | Definition | Why it matters |
|---|---|---|
| Objective vs baseline | Cost, wait time or late jobs vs the current plan or a simple rule | The number the business sees |
| Optimality gap | (incumbent objective minus best proven bound) divided by incumbent | How far from optimal the plan can be. Solvers such as [CP-SAT](https://d-krupke.github.io/cpsat-primer/) report the bound |
| Solve time | Time to reach a set gap, on production-sized instances | A plan that arrives after the shift starts is worthless |
| Feasibility on real constraints | Share of plans the floor can run without edits | Models miss rules nobody wrote down |
| Plan churn | Assignments changed vs the previous plan | Stability is what makes re-plans usable |
| Tail cost | P95 or P99 cost across simulated scenarios | The mean hides the bad year |

How to test each:

| Test | How |
|---|---|
| Feasibility | Replay last month's real orders through the model. Have planners mark every plan they would have edited, and why. Each "why" is a missing constraint |
| Stability | Re-plan after one realistic change (a late truck, a machine down) and count moved assignments. [Demo 05](../../implementations/05-dock-scheduling): the optimal re-plan moved 7 trucks, the stable one moved 1 |
| Tail risk | Simulate disruptions and report percentiles. [Demo 10](../../implementations/10-dual-sourcing): dual sourcing costs 3.8% more on average and 9.7% less in a 1-in-20 year |
| Objective design | Compare objectives, not just solvers. [Demo 11](../../implementations/11-changeover-scheduling): adding due dates to the objective cut late jobs from 2 to 1 at no extra changeover |
| Scale | Test on instances as large as production. CVRPLIB's X set runs from 100 to 1,000 customers ([Uchoa et al. 2017](https://doi.org/10.1016/j.ejor.2016.08.012)); toy instances flatter learned methods |

For LLM-formulated models, add a check that the model matches the problem: compare its answers to a hand-built model on a set of known cases. A formulation can be solved to optimality and still be the wrong formulation ([Large Language Model enabled Mathematical Modeling](https://arxiv.org/abs/2510.19895) builds a hallucination taxonomy for exactly this).

## Agents

| Metric | Definition |
|---|---|
| Safe success | Goal reached with zero policy violations. Rank on this |
| Violations | Calls outside the allowed list; money or commitments without approval |
| pass^k | Share of tasks solved on all k repeated runs ([τ-bench](https://arxiv.org/abs/2406.12045), background) |
| Cost per case | Model spend plus tool calls plus human minutes spent on the case |
| Human escalation rate | Share of cases handed to a person |
| Escalation precision | Share of escalations a reviewer agrees were needed |
| Missed escalations | Cases the agent closed that a reviewer says should have gone to a person |
| Time to resolution | Case open to case closed |

How to build the test set:

| Include | Why |
|---|---|
| Tasks where the right action is to do nothing | Catches over-acting. SCX-Bench's late-but-fits truck |
| A tempting shortcut in every task | Catches the money shortcut. SCX-Bench's eager agent breaks policy on every task and scores zero safe successes |
| Messy, plain-language messages | Real carrier emails, not clean prompts |
| Planted instructions in emails and documents | Prompt injection tests, as in [AgentDojo](https://arxiv.org/abs/2406.13352) |
| Repeated runs per task | One pass proves little; agents vary run to run ([agent bullwhip](https://arxiv.org/abs/2605.17036)) |

Run [demo 06](../../implementations/06-agent-with-guardrails) to see the guardrail layer, then score your agent on [SCX-Bench](../../benchmark) and on tasks drawn from your own closed cases. Design details are in the [agent architecture playbook](agent-architecture.md).

## Document AI

| Metric | Definition |
|---|---|
| Field precision | Of the values the model extracted for a field, the share that are correct |
| Field recall | Of the values present in the document, the share the model extracted correctly |
| Exact vs normalized match | Score "9,100 kg" vs "9100" as the same only if your system treats them the same |
| Straight-through rate | Share of documents that pass every validation rule with no human touch |
| Residual error rate | Share of straight-through documents that still contain an error. The number that matters to finance |
| False alarm rate | Share of clean documents sent to a human anyway |

Score per field, not per document. A model that is 99% right on consignee and 70% right on weight has a weight problem, and an average hides it.

Validation rules are part of the system under test. In [demo 13](../../implementations/13-document-validation), 13.7% of documents carry an extraction error; four cheap rules catch 80.1% of them, straight-through rate is 87.8%, and the error rate in straight-through documents falls to 3.1%. The rules miss most swapped weight digits (28% caught), which tells you which rule to add next.

For a public benchmark on business documents (key information extraction and line items), see [DocILE](https://arxiv.org/abs/2302.05658).

## Offline vs online

| Stage | What it answers | What it cannot answer |
|---|---|---|
| Backtest or benchmark | Is it better than the baseline on history? | How people and partners react |
| Shadow mode | Would its decisions have been better than what people did, on today's data? | The effect of acting on its decisions |
| Controlled live test | Does acting on it improve the business metric? | Long-run effects, unless you run it long enough |
| Holdout after launch | Is it still better six months later? | Nothing new; it is the drift check |

### Shadow mode

The model or agent runs on live data and proposes; people keep deciding. Log both. Compare proposals with human decisions and, once outcomes are known, with what actually happened. Shadow mode is cheap, catches data pipeline bugs, and shows where the model disagrees with experts. Its limit: it scores the model against the world people created, not the world the model would have created.

### A/B tests and their supply chain problem

Randomizing per order or per shipment often breaks in logistics, because units share capacity. Two arms that share docks, trucks, pickers or stock affect each other. A dock schedule tested on half the trucks changes the wait for the other half.

| Design | When it fits |
|---|---|
| Randomize by order or shipment | Units do not share capacity (for example, customer reply wording) |
| Randomize by site, lane or region | Sites are independent enough; accept fewer units and wider intervals |
| Switchback (alternate treatment over time blocks) | One shared system, such as one DC or one dispatch desk. [Bojinov, Simchi-Levi and Zhao](https://arxiv.org/abs/2009.00148) derive designs that account for carryover between blocks |
| Before and after with a matched control site | Only option when the change is site-wide; weakest evidence |

Write down the metric, the guardrail metrics (service level, cost, violations) and the stop rule before the test starts. For background on running controlled experiments well, see Kohavi, Tang and Xu, [Trustworthy Online Controlled Experiments](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59) (Cambridge University Press, not free).

## Common traps

| Trap | Fix |
|---|---|
| Reporting accuracy, deciding on cost | Report both; decide on the business metric |
| Comparing to a weak baseline | Always include seasonal naive, the current plan, or the rule-based agent |
| One holdout window | Rolling origins |
| Toy instances | Production-sized instances from your own history |
| Average-only reporting | Add P95 or P99 and per-segment results |
| Scoring the agent once | Repeated runs, pass^k |
| Counting a closed case as success | Safe success: closed and within policy |
| Document accuracy as one number | Per field, plus residual error in straight-through documents |
| Shadow mode forever | Set the date and the bar for a live test in advance |

## Sources
- Hyndman and Athanasopoulos, [Forecasting: Principles and Practice, 3rd ed.](https://otexts.com/fpp3/) (free online).
- Hyndman and Koehler (2006), [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001).
- Makridakis, Spiliotis and Assimakopoulos (2022), [M5 accuracy competition: results, findings, and conclusions](https://doi.org/10.1016/j.ijforecast.2021.11.013).
- Aksu et al. (2024), [GIFT-Eval](https://arxiv.org/abs/2410.10393).
- [Beyond Accuracy: Are Time Series Foundation Models Well-Calibrated?](https://arxiv.org/abs/2510.16060) (2025).
- [Rethinking Evaluation in the Era of Time Series Foundation Models: (Un)known Information Leakage Challenges](https://arxiv.org/abs/2510.13654) (2025).
- Uchoa et al. (2017), [New benchmark instances for the Capacitated Vehicle Routing Problem](https://doi.org/10.1016/j.ejor.2016.08.012).
- Yao et al. (2024), [τ-bench](https://arxiv.org/abs/2406.12045); Debenedetti et al. (2024), [AgentDojo](https://arxiv.org/abs/2406.13352).
- Šimsa et al. (2023), [DocILE Benchmark for Document Information Localization and Extraction](https://arxiv.org/abs/2302.05658).
- Bojinov, Simchi-Levi and Zhao, [Design and Analysis of Switchback Experiments](https://arxiv.org/abs/2009.00148).
