# Playbook: from pilot to production

How a supply chain organisation gets an AI system from a demo to something planners, dispatchers and floor teams use every day. Most of this is not about models.

The base rate is not encouraging. Gartner predicted in June 2025 that over 40% of agentic AI projects will be cancelled by the end of 2027, citing escalating costs, unclear business value or inadequate risk controls ([Gartner press release](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)). The steps below are aimed at all three causes.

## The path

| Stage | Exit when | Typical length |
|---|---|---|
| 1. Pick the use case | Problem type named, baseline measured, owner agreed | Weeks |
| 2. Offline proof | Beats the baseline on history, on the business metric | Weeks |
| 3. Shadow mode | Proposals compared with real decisions on live data; pipeline stable | One or more full business cycles |
| 4. Limited live | Acts on a slice (one site, lane, category) with approvals; controlled comparison | One or more cycles |
| 5. Scale | Metric holds across slices; monitoring and ownership in place | Ongoing |
| 6. Review or stop | Periodic check against the kill criteria | Every quarter |

"Typical length" is guidance from the shape of the work, not a measured benchmark. A business cycle is whatever repeats in your operation: a week for dock scheduling, a month for a financial close, a season for retail demand.

## 1. Picking the first use case

Score candidates on five questions. The best first project scores well on all five, not brilliantly on one.

| Question | Good sign | Warning sign |
|---|---|---|
| What type of problem is it? | Clear: prediction, planning, coordination, documents or shared truth ([fit guide](../technology/fit-guide.md)) | "We want to use GenAI somewhere" |
| Is the data ready? | The inputs exist in a system, with history, and someone knows what the fields mean | Key inputs live in spreadsheets, email or people's heads |
| Is there a measurable baseline? | Today's number is known: forecast error, wait minutes, cost per case, touches per document | Nobody measures the current process |
| Who owns the decision? | A named team that will use the output and is asked to | The output goes to a dashboard nobody owns |
| What does a wrong answer cost? | Bounded and reversible: a draft email, a suggested slot | Irreversible or regulatory: customs filings, payments |

Good first candidates by problem type, all with a demo in this repo:

| Use case | Type | Why it is a good start | Demo |
|---|---|---|---|
| Safety stock review | Planning | Cheap to test against history; often reveals lead-time variability nobody modelled | [09](../../implementations/09-safety-stock) |
| ETA windows | Prediction | Outcomes arrive daily, so you learn fast | [12](../../implementations/12-eta-calibration) |
| BOL or invoice checks | Documents | Rules plus extraction; baseline is manual keying | [13](../../implementations/13-document-validation) |
| POD chasing | Coordination | High volume, low risk per case, clear success state | [06](../../implementations/06-agent-with-guardrails) |
| Dock re-plans | Planning | Visible to the floor; stability matters | [05](../../implementations/05-dock-scheduling) |

Also consider whether you need machine learning at all. Google's [Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) starts with "Don't be afraid to launch a product without machine learning". A validation rule or a better safety stock formula is often the first win.

## 2. Pilot design

Write this down before any code. One page is enough.

| Item | Example |
|---|---|
| Decision being changed | Which dock door and time each inbound truck gets |
| Scope | One DC, inbound only, day shift |
| Baseline metric and current value | Average truck wait, measured over the last 8 weeks |
| Target | A stated improvement, chosen before the pilot |
| Guardrail metrics | Trucks moved per re-plan, missed appointments, overtime |
| Comparison | Switchback by day, or a matched control DC ([evaluation](evaluation.md#ab-tests-and-their-supply-chain-problem)) |
| Kill criteria | Guardrail metric worse for two consecutive weeks; floor team stops using it |
| Owner | Named site operations lead, not the data team |

## 3. Shadow mode

The system runs on live data and proposes. People decide as they do today. Both are logged.

| Do | Why |
|---|---|
| Run for at least one full business cycle | Monday peaks, month-end and promotions all show up |
| Compare proposals with human decisions daily | Disagreements are the most useful data you will get |
| Ask the people who decided to review the disagreements | They know the constraint the model missed |
| Track pipeline failures | Missing feeds and late files show up in shadow mode, not in a backtest |
| Fix the date and the bar for going live | Shadow mode with no exit becomes the permanent state |

For agents, shadow mode means the agent drafts every message and proposes every action, and a person sends or executes. This is also where you measure how often the person changes the draft.

## 4. Change management with planners and floor teams

The people who run the operation decide whether the system gets used. Two findings from the research are worth designing around.

| Finding | Source | Design response |
|---|---|---|
| Planners routinely adjust system forecasts. In a study of more than 60,000 forecasts at four supply chain companies, adjustments improved accuracy on average in three of them, but larger adjustments helped while small ones often hurt, and upward adjustments were more often wrong (optimism bias) | [Fildes et al. 2009](https://doi.org/10.1016/j.ijforecast.2008.11.010) | Keep overrides, log them, and measure whether each kind of override improves the outcome. Discourage small tweaks |
| People lose trust in an algorithm faster than in a person after seeing it make the same mistake | [Dietvorst, Simmons and Massey 2015](https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/20-Dietvorst-Simmons-Massey-2015.pdf) | Show the error record of the current process next to the model's; expect visible mistakes and plan the response |
| People are more willing to use an imperfect algorithm if they can adjust its output, even slightly | [Dietvorst, Simmons and Massey 2018](https://ideas.repec.org/a/inm/ormnsc/v64y2018i3p1155-1170.html) | Give a bounded override (for example, plus or minus 10%) instead of all or nothing |

Practical rules:

| Rule | Why |
|---|---|
| Involve the planners in choosing the baseline and the metric | They will not trust a metric someone else picked |
| Explain every output in the user's terms | "Moved to door 4 because truck 7 is 50 minutes late", not a score |
| Prefer stable plans over slightly better ones | A plan the floor can follow beats an optimal plan it ignores ([demo 05](../../implementations/05-dock-scheduling)) |
| Make the override easy and logged | Hidden workarounds (spreadsheets, phone calls) remove your feedback |
| Do not measure people on agreeing with the model | They will agree, and you will lose the signal |
| Tell floor teams what changes for them, in their shift briefing | Dispatchers, yard drivers and pickers feel the change first |
| Say what the system will not do | It will not pay, promise dates or cancel orders. Fear of the unknown slows adoption |

## 5. Ownership

| Role | Owns |
|---|---|
| Business owner (operations, planning, procurement) | The decision, the metric, the allowed actions, go and stop calls |
| Product or process owner | Pilot design, rollout, training, the feedback loop with users |
| Data and ML team | Models, pipelines, evaluation, monitoring |
| IT and integration | Connections to TMS, WMS, ERP, EDI and email; access control |
| Risk, finance, compliance | Approval thresholds, audit log requirements, regulatory documents |
| Partner managers (carrier, supplier) | What outside parties are told, and how |

If the business owner box is empty, do not start. A model with no owner becomes a dashboard.

## 6. Monitoring and drift

Supply chains change underneath models: new lanes, new carriers, a tariff, a new DC, a promotion calendar. Concept drift, where the link between inputs and outcome changes over time, is a well-studied problem ([Gama et al. 2014](https://eprints.bournemouth.ac.uk/22491/)). The surrounding system usually causes more trouble than the model: [Sculley et al. 2015](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) describe how data dependencies, feedback loops and configuration make ML systems costly to maintain.

| Monitor | Example signal | Action |
|---|---|---|
| Input data | Missing feeds, late files, new codes, unit changes | Alert the pipeline owner; fall back to the baseline |
| Input distribution | New lane mix, new SKU share, demand level shift | Review; retrain if the outcome metric moves |
| Outcome metric | Forecast error, late share inside the ETA window, wait time | Compare to baseline every week |
| Calibration | Interval coverage drifts from its target | Recalibrate (conformal recalibration is cheap: [demo 12](../../implementations/12-eta-calibration)) |
| Usage | Override rate, ignored proposals, workaround spreadsheets | Talk to users before touching the model |
| Agent behaviour | Violations blocked, approvals denied, escalation rate, cost per case | Review the cases; tighten tools or allowed lists |
| Feedback loops | The model's own decisions now shape its training data (for example, stock it chose drives the sales it sees) | Keep a small holdout or randomized slice |

Keep the baseline running in the background. It is your fallback and your yardstick.

## 7. When to stop

Stopping a project that is not working is a result, not a failure. Agree the stop rules at the start.

| Stop or rescope when | Example |
|---|---|
| It does not beat the baseline on the business metric after a fair test | The new ETA model is more accurate but late-truck share is unchanged |
| The gain is smaller than the cost of running it | Model, integration and review time exceed the savings |
| Users route around it | Planners keep a parallel spreadsheet |
| The data needed does not exist and will not soon | Supplier lead times are not recorded anywhere |
| The risk cannot be bounded | The agent needs payment rights to be useful |
| The problem was the wrong type | An LLM asked to produce a plan; switch to a solver |

## Autonomy ladder

Grant autonomy one rung at a time, per action, not per system.

| Rung | The system | People |
|---|---|---|
| 1. Suggest | Proposes; nothing executes | Decide and act |
| 2. Draft | Prepares the action or message | Approve each one |
| 3. Act within limits | Executes low-risk actions inside thresholds | Approve money and commitments; review samples |
| 4. Act and report | Executes; reports exceptions | Review exceptions and metrics |

A POD request email might reach rung 4. A detention payment should stay at rung 2. [Agentic AI Autonomy Assessment](https://arxiv.org/abs/2607.25405) (2026) proposes measuring autonomy per task, which fits this per-action view. The design of the guardrails at each rung is in the [agent architecture playbook](agent-architecture.md).

## Sources
- Gartner (25 June 2025), [Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027).
- Google, [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml).
- Fildes, Goodwin, Lawrence and Nikolopoulos (2009), [Effective forecasting and judgmental adjustments: an empirical evaluation and strategies for improvement in supply-chain planning](https://doi.org/10.1016/j.ijforecast.2008.11.010), International Journal of Forecasting.
- Dietvorst, Simmons and Massey (2015), [Algorithm aversion: people erroneously avoid algorithms after seeing them err](https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/20-Dietvorst-Simmons-Massey-2015.pdf), Journal of Experimental Psychology: General.
- Dietvorst, Simmons and Massey (2018), [Overcoming algorithm aversion: people will use imperfect algorithms if they can (even slightly) modify them](https://ideas.repec.org/a/inm/ormnsc/v64y2018i3p1155-1170.html), Management Science.
- Gama et al. (2014), [A survey on concept drift adaptation](https://eprints.bournemouth.ac.uk/22491/), ACM Computing Surveys.
- Sculley et al. (2015), [Hidden technical debt in machine learning systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems), NeurIPS.
