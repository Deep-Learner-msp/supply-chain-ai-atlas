# 03. Make: production and scheduling

Make turns materials into finished goods: what to produce, on which line, in which order, and when to change over. It is owned by plant management, production planning and scheduling, maintenance and quality. It matters because the plant is where most of the fixed cost of a supply chain sits. An hour of lost line time cannot be bought back, and a schedule that ignores changeovers or a failing machine breaks every promise made downstream in [Move](04-move.md) and [Deliver](06-deliver.md).

Most of Make is a **Planning** problem (hard constraints, a cost to minimize) with **Prediction** problems feeding it (machine failure, processing time, yield). Name the type first: see the [fit guide](../technology/fit-guide.md).

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Plant and line capacity, make or buy | Strategic | Operations leadership, network design | Yearly |
| Master production schedule (what, how much, which week) | Tactical | Master scheduler, S&OP | Weekly to monthly |
| Lot sizing and campaign length | Tactical | Production planning | Weekly |
| Detailed sequence on each line, including changeovers | Operational | Scheduler | Daily or per shift |
| Rescheduling after a breakdown, rush order or late material | Operational | Scheduler, shift lead | As events happen |
| Maintenance windows (preventive versus run to failure) | Tactical and operational | Maintenance planner | Weekly, plus on alarm |
| Quality hold, rework or scrap | Operational | Quality engineer | Per batch |
| Staffing and skills per shift | Tactical | Plant HR, shift managers | Weekly |

## KPIs
| Metric | Definition | Why it matters |
|---|---|---|
| OEE (overall equipment effectiveness) | Availability x Performance x Quality ([definition](https://www.oee.com/calculating-oee/)). Example: 0.90 x 0.95 x 0.98 = 0.838 | One number for how much of planned time made good product. Each factor points to a different fix |
| Availability | Run time / planned production time | Captures breakdowns and changeovers |
| Performance | (Ideal cycle time x total count) / run time | Captures slow cycles and small stops |
| Quality (first-pass yield) | Good count / total count | Scrap and rework cost capacity twice |
| Schedule adherence | Orders (or quantity) produced in the planned slot / orders planned for that slot | Tells you whether the schedule is a plan or a wish |
| Changeover time | Time from last good unit of the old product to first good unit of the new one ([SMED](https://en.wikipedia.org/wiki/Single-minute_exchange_of_die)) | The capacity you lose every time the sequence changes |
| Makespan | Time from the start of the first job to the end of the last | The textbook scheduling objective. Real plants care more about tardiness |
| Total tardiness, on-time completion | Sum of lateness past due dates; share of orders done by due date | What the customer and [Move](04-move.md) actually feel |
| Mean time between failures (MTBF), mean time to repair (MTTR) | Run time / number of failures; repair time / number of repairs | The inputs to any maintenance decision |
| Work in process (WIP) and cycle time | Units in the system; time a unit spends in it. Linked by [Little's law](https://en.wikipedia.org/wiki/Little%27s_law) (WIP = throughput x cycle time) | High WIP hides problems and slows everything |

## Data and systems
| System | What it holds | Standard |
|---|---|---|
| ERP | Orders, bills of materials, routings, costs | [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard) level 4 |
| APS (advanced planning and scheduling) | Finite-capacity plans and sequences | Sits between levels 3 and 4 |
| MES (manufacturing execution system) | Work orders released, actual start and end times, scrap, genealogy | ISA-95 level 3; see [MESA](https://www.mesa.org/) |
| Batch control | Recipes and phases in process plants | [ISA-88](https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards) |
| SCADA, PLC historians | Sensor time series, alarms, machine states | ISA-95 levels 1 and 2 |
| CMMS | Work orders, failure codes, spare parts | |
| QMS, vision stations | Inspection results, images, non-conformance reports | |

The common data problem: the ERP routing says a changeover takes 30 minutes, the MES says it took 75, and nobody has reconciled the two. Fix the master data before training anything on it.

## Classical methods that work
This is the baseline any AI method has to beat, on the same instances, with the same time limit.

| Method | Use it for | Reference |
|---|---|---|
| Dispatching rules (EDD, SPT, ATCS for sequence-dependent setups) | Fast, explainable sequencing; the fallback when everything else fails | [Pinedo, *Scheduling*, 6th ed.](https://link.springer.com/book/10.1007/978-3-031-05921-6) |
| Constraint programming (CP-SAT) with interval variables, no-overlap and transition times | Detailed scheduling with changeovers, calendars and resources | [OR-Tools job shop guide](https://developers.google.com/optimization/scheduling/job_shop), [CP-SAT primer](https://github.com/d-krupke/cpsat-primer) |
| MILP lot-sizing models | Campaign length and master scheduling | [Pyomo](https://github.com/Pyomo/pyomo), [PuLP](https://github.com/coin-or/pulp) |
| Metaheuristics (tabu search, genetic algorithms, large neighbourhood search) | Very large or messy instances | Pinedo, part III |
| SMED (single-minute exchange of die) | Cutting changeover time itself, before optimizing around it | [SMED overview](https://en.wikipedia.org/wiki/Single-minute_exchange_of_die) |
| Factory physics and Little's law | Sizing WIP, buffers and capacity | Hopp and Spearman, [*Factory Physics*](https://en.wikipedia.org/wiki/Factory_Physics) |
| Time-based and condition-based maintenance | Maintenance with thresholds on vibration, temperature, hours | Standard reliability practice |

Standard benchmark instances: [JSPLIB](https://github.com/tamy0612/JSPLIB) (job shop, including Taillard), [PSPLIB](https://www.om-db.wi.tum.de/psplib/) (project scheduling).

## What fits
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Production scheduling and sequencing | Planning | Constraint programming (CP-SAT), MILP, learned heuristics as warm starts | An LLM writing the schedule directly |
| Rescheduling after a disruption | Planning | Re-solve with a penalty for moving jobs that were already fixed | A fresh optimal plan that moves everything |
| Explaining a schedule, what-if questions | Planning + language | LLM over solver output | LLM answers with no solver behind them |
| Formulating a new scheduling model | Planning + language | LLM drafts, solver checks, engineer reviews | Shipping LLM-written model code without tests |
| Predictive maintenance | Prediction | Sensor models, anomaly detection, survival models on failure history | Predicting failures with no labelled failures and no plan for acting on the alarm |
| Processing time and yield prediction | Prediction | Gradient-boosted trees on MES history | Using routing standards that were never updated |
| Maintenance work orders and failure notes | Documents | LLM extraction into failure codes, with validation | Free text left in the CMMS |
| Quality inspection | Documents/vision | Computer vision, anomaly detection trained on good parts | Vision models with no human review of rejects |

## AI in practice, 2025 to 2026
| Claim | Verdict | Evidence |
|---|---|---|
| "LLMs can schedule a factory" | Not yet as the engine. Results are usually against dispatching rules or neural baselines, not against a tuned CP solver | [Starjob](https://arxiv.org/abs/2503.01877) fine-tunes an 8B model and compares with priority dispatching rules and L2D, not CP-SAT. [SCHEDBench](https://arxiv.org/abs/2608.00991) finds 13 LLMs give different feasibility on reworded versions of the same problem |
| "LLMs can write the scheduling model for you" | Useful as a draft. Formulation is close; runnable code is not | [Agentic modelling in CP](https://arxiv.org/abs/2610.10184): runnable scripts rise from 14.8% (direct LLM call) to 59.3% with a multi-agent workflow on six industrial problems. Four in ten still fail |
| "Agents can repair broken optimization models" | Promising with training and solver feedback | [OptiRepair](https://arxiv.org/abs/2602.19439): trained 8B models reach 81.7% rational recovery versus 42.2% for the best API model |
| "LLMs write better heuristics than experts" | Not on average | [HeuriGym](https://arxiv.org/abs/2506.07972): top models score about 0.6 on its quality-yield index against an expert baseline of 1 |
| "Learned solvers beat classical ones" | Mostly not at real scale | [FrontierCO](https://arxiv.org/abs/2505.16952) finds a gap that widens on large, structured instances, with some exceptions |
| "Deep RL for flexible job shops" | Competitive in research environments; little public evidence on live plants | [Efficient DRL environment for FJSP](https://arxiv.org/abs/2509.07019) reports results competitive with OR-Tools on public instances |
| "Agents for maintenance and asset operations" | Early. Benchmarks show brittle reasoning | [AssetOpsBench](https://arxiv.org/abs/2506.03828), [FailureSensorIQ](https://arxiv.org/abs/2506.03278) (performance drops under perturbations), [CODS 2025 challenge retrospective](https://arxiv.org/abs/2605.08518) (public and hidden execution scores do not agree) |

The working pattern is the same as everywhere in this atlas: the solver computes, the LLM translates and explains, a person approves.

## Worked example: changeover sequencing
*Illustrative numbers.* One filling line runs four products each day. Changeover minutes depend on the order (rows: from, columns: to):

| From \ To | A light | B medium | C dark | D allergen |
|---|---|---|---|---|
| A light | | 20 | 40 | 90 |
| B medium | 45 | | 25 | 90 |
| C dark | 60 | 50 | | 90 |
| D allergen | 120 | 120 | 120 | |

- **Order of arrival** C, A, D, B: 60 + 90 + 120 = **270 minutes** of changeover.
- **Best sequence** A, B, C, D (light to dark, allergen last): 20 + 25 + 90 = **135 minutes**. This is the minimum over all 24 orders.
- Saving: 135 minutes a day. Over 5 days, 675 minutes (11.25 hours) a week. If an hour of line time is worth $1,800 in contribution, that is $20,250 a week.

What to notice:
- The classic rule of thumb (light to dark, allergen last) already finds the optimum here. That is the baseline an AI method must beat.
- The rule breaks once due dates conflict with the ideal order, or when two lines share one cleaning crew. That is where a CP solver earns its place: it trades changeover minutes against tardiness explicitly.
- Run a version with due dates and a solver in [11-changeover-scheduling](../../implementations/11-changeover-scheduling).

## Common mistakes
- Optimizing makespan when the plant is measured on on-time completion.
- Scheduling with routing standards nobody has checked against the MES.
- Re-solving from scratch after every event, so the floor sees a new plan every hour. Penalise moving jobs (see [05-dock-scheduling](../../implementations/05-dock-scheduling) for the same idea at the dock).
- Reporting a learned scheduler's gap against dispatching rules instead of against a tuned CP-SAT or MILP model with the same time limit.
- Predictive maintenance pilots that predict well but have no maintenance slot, spare part or technician to act on the prediction.
- Treating OEE as a target to game rather than a diagnosis. Moving more hours out of "planned production time" raises OEE without making one more unit.
- Letting an LLM change a model or a schedule with no feasibility check before it reaches the floor.

## Run it
- [11-changeover-scheduling](../../implementations/11-changeover-scheduling): production scheduling with sequence-dependent changeovers, CP-SAT.
- [05-dock-scheduling](../../implementations/05-dock-scheduling): CP-SAT scheduling and why stable re-plans beat optimal ones.
- [04-llm-solver-interface](../../implementations/04-llm-solver-interface): the LLM translates the question, the solver computes the answer.

## Key papers
Full list: [papers](../../papers/2025-2026.md#planning-and-optimization).

| Paper | Why read it |
|---|---|
| [Starjob: Dataset for LLM-Driven Job Shop Scheduling](https://arxiv.org/abs/2503.01877) (2025) | 130k job-shop instances for training LLMs; note the baselines it compares against |
| [SCHEDBench](https://arxiv.org/abs/2608.00991) (2026) | Do LLM schedules stay feasible when the same problem is worded differently? Often not |
| [Agentic AI-Assisted Modeling for Production Scheduling: Assessment in Constraint Programming](https://arxiv.org/abs/2610.10184) (2026) | Honest numbers on LLM agents writing CP models for flow, job and flexible job shops |
| [DScheLLM](https://arxiv.org/abs/2601.09100) (2026) | Fine-tuned LLM for dynamic job-shop rescheduling, trained on solver-generated schedules |
| [ALAS: A Stateful Multi-LLM Agent Framework for Disruption-Aware Planning](https://arxiv.org/abs/2505.12501) (2025) | Agents with state and local repair for job-shop disruptions |
| [Self-Evaluation for Job-Shop Scheduling](https://arxiv.org/abs/2502.08684) (2025) | Neural job-shop method that scores subsets of assignments to limit error build-up |
| [An efficient deep reinforcement learning environment for flexible job-shop scheduling](https://arxiv.org/abs/2509.07019) (2025) | Why the environment design matters as much as the agent |
| [HeuriGym](https://arxiv.org/abs/2506.07972) (2025) | LLM-written heuristics scored against expert baselines |
| [CO-Bench](https://arxiv.org/abs/2504.04310) (2025) | LLM agents searching for combinatorial optimization algorithms |
| [OptiRepair](https://arxiv.org/abs/2602.19439) (2026) | Agents that diagnose and repair infeasible optimization models |
| [FrontierCO](https://arxiv.org/abs/2505.16952) (2025) | Learned solvers versus classical ones at real scale, scheduling included (listed in the papers file under its earlier title) |
| [AssetOpsBench](https://arxiv.org/abs/2506.03828) (2025) | Benchmark for agents in industrial asset operations and maintenance |
| [FailureSensorIQ](https://arxiv.org/abs/2506.03278) (2025) | Do LLMs understand sensors and failure modes? Fragile under perturbation |
| [Results and Retrospective Analysis of the CODS 2025 AssetOpsBench Challenge](https://arxiv.org/abs/2605.08518) (2026) | What a public leaderboard hides; the successful execution methods mostly improved guardrails |

## Tools and datasets
| Tool or dataset | Use | Where |
|---|---|---|
| OR-Tools CP-SAT | Scheduling with intervals and transition times | [google/or-tools](https://github.com/google/or-tools), [CP-SAT guide](https://developers.google.com/optimization/cp/cp_solver) |
| CP-SAT primer | Hands-on scheduling modelling | [d-krupke/cpsat-primer](https://github.com/d-krupke/cpsat-primer) |
| CPMpy, MiniZinc | Solver-independent constraint modelling | [CPMpy/cpmpy](https://github.com/CPMpy/cpmpy), [minizinc.org](https://www.minizinc.org/) |
| Pyomo, PuLP | MILP lot sizing | [Optimization tools](../../repos/README.md#optimization-and-routing) |
| RL4CO | RL baselines for scheduling and routing | [ai4co/rl4co](https://github.com/ai4co/rl4co) |
| JSPLIB, PSPLIB | Standard job-shop and project scheduling instances | [JSPLIB](https://github.com/tamy0612/JSPLIB), [PSPLIB](https://www.om-db.wi.tum.de/psplib/) |
| Starjob | LLM job-shop training data | [datasets](../../datasets/README.md) |
| AI4I 2020 | Synthetic predictive maintenance data | [UCI](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) |
| C-MAPSS | Simulated turbofan degradation, remaining useful life | [NASA](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data) |
| MVTec AD | Visual anomaly detection on industrial parts | [MVTec](https://www.mvtec.com/company/research/datasets/mvtec-ad) |
| AssetOpsBench, FailureSensorIQ | Agent and LLM benchmarks for maintenance | [IBM/AssetOpsBench](https://github.com/IBM/AssetOpsBench), [IBM/FailureSensorIQ](https://github.com/IBM/FailureSensorIQ) |

## Open problems
- LLM-written heuristics look good on benchmarks; plant constraints are messier.
- Verifying that an LLM-formulated model matches the real plant (see [open problems](../open-problems.md), #5). Runnable is not the same as correct: a model can solve and still miss a cleaning rule.
- **Wording sensitivity.** The same scheduling problem phrased two ways gives different feasibility ([SCHEDBench](https://arxiv.org/abs/2608.00991)). Planners will not phrase requests the way a benchmark does.
- **Stability versus optimality in rescheduling.** There is no agreed metric for how much plan churn a floor can absorb, so methods are scored on cost alone.
- **Public benchmarks with real plant structure.** Job-shop instances have no changeover matrices, shared crews, calendars or material arrival. Most learned-scheduler results come from instances without them.
- **Maintenance that closes the loop.** A failure prediction is only worth something if it changes the schedule. Joint prediction and scheduling is rarely evaluated end to end.

## Further reading
- Michael Pinedo, [*Scheduling: Theory, Algorithms, and Systems*](https://link.springer.com/book/10.1007/978-3-031-05921-6), 6th ed., Springer, 2022.
- Wallace Hopp and Mark Spearman, [*Factory Physics*](https://en.wikipedia.org/wiki/Factory_Physics): variability, WIP and capacity from first principles.
- MIT OpenCourseWare, [15.760B Introduction to Operations Management](https://ocw.mit.edu/courses/15-760b-introduction-to-operations-management-spring-2004/).
- MITx [MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM) (MIT Learn, free to audit).
- Standards: [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard) (enterprise and control integration), [ISA-88](https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards) (batch control), [MESA International](https://www.mesa.org/), [ASCM SCOR Digital Standard](https://www.ascm.org/corporate-transformation/standards-tools/scor-ds/).
