# 04. Move: transport and routing

Move gets goods from where they are to where they are needed: which mode and carrier, which route, when to tender, and how to recover a late load. It is owned by transportation and logistics teams at shippers, by carriers and brokers, and often by a third-party logistics provider in between. It matters because transport is a large, visible cost and the step where most handoffs between companies happen. Every handoff is a message, a document and a chance for the plan to drift from reality.

Move mixes all five problem types in the [fit guide](../technology/fit-guide.md): **Planning** (routes, loads), **Prediction** (ETAs, rates, acceptance), **Coordination** (tenders, follow-ups, appointments), **Documents** (bills of lading, proof of delivery, invoices) and **Shared truth** (who agrees on what happened, and when).

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Mode mix and network (own fleet, contract carriers, brokers, intermodal) | Strategic | Logistics leadership | Yearly |
| Carrier procurement and lane awards | Tactical | Transport procurement | Yearly, with mini-bids each quarter |
| Routing guide (primary and backup carriers per lane) | Tactical | Transport planning | Quarterly |
| Load building and consolidation | Operational | Load planner, TMS | Daily |
| Tendering, and when to go to the spot market | Operational | Planner, broker desk | Per load |
| Vehicle routing and dispatch (own fleet) | Operational | Dispatcher | Daily, re-planned during the day |
| Appointment booking at pickup and delivery | Operational | Planner, facility scheduler | Per load |
| Exception recovery (late, rejected, damaged load) | Operational | Control tower, carrier rep | As events happen |
| Freight audit and payment | Operational | Finance, freight audit provider | Per invoice |

## KPIs
| Metric | Definition | Why it matters |
|---|---|---|
| On-time pickup (OTP) | Loads picked up within the appointment window / loads picked up | Late pickups become late deliveries and missed dock slots in [Store](05-store.md) |
| On-time delivery (OTD) | Loads delivered within the appointment window / loads delivered | The service metric customers and retail compliance programmes score |
| Cost per mile | Total operating cost / miles driven. ATRI's US industry average for 2025 was $2.336 ([ATRI, 2026](https://truckingresearch.org/2026/07/new-atri-report-details-accelerating-costs-and-low-profitability-despite-cuts/)) | The carrier's basic unit economics, and the anchor for rate negotiations |
| Empty miles (deadhead) | Miles driven without a paying load / total miles | Paid for but earns nothing. Network design and backhaul matching attack it |
| Tender acceptance rate | Tenders accepted by the assigned carrier / tenders offered to that carrier | Falls when the market tightens. Every rejection pushes a load down the routing guide or to the spot market |
| Dwell time | Departure time minus arrival time at a facility | The visible symptom of dock and appointment problems |
| Detention | Time a driver waits at a facility beyond the scheduled appointment or free time, usually billed per hour | A cost to the shipper, lost hours to the carrier, and a safety issue (see below) |
| ETA accuracy | Mean absolute error of predicted versus actual arrival; for intervals, the share of arrivals inside the stated interval (coverage) | A point ETA without a calibrated range cannot be planned around |
| Load factor | Weight or cube used / truck capacity | Under-filled trucks raise cost per unit shipped |
| Invoice accuracy | Invoices that match the agreed rate and accessorials / invoices received | Mismatches drive freight audit work and disputes |

### Detention, in numbers
ATRI surveyed 587 drivers at the 2024 Mid-America Trucking Show. They reported being detained at **39.3% of stops in 2023**, and detention cost the industry $3.6 billion in direct expenses and $11.5 billion in lost productivity. Fleets that charge detention fees are paid for fewer than half of those invoices ([ATRI, September 2024](https://truckingresearch.org/2024/09/new-research-documents-substantial-financial-and-safety-impacts-from-truck-driver-detention/); sample details in [Transport Topics](https://www.ttnews.com/articles/atri-driver-detention-2023)). The figure is driver-reported survey data, not a measured census. Most of that waiting is a coordination problem, not a prediction problem.

## Data and systems
| System or message | What it carries | Standard |
|---|---|---|
| TMS (transportation management system) | Orders, loads, carriers, rates, routing guide, tender status | |
| Load tender and response | Shipper offers a load; carrier accepts or rejects | [X12](https://x12.org/products/transaction-sets) 204 Motor Carrier Load Tender, 990 Response to a Load Tender |
| Shipment status | Pickup, in transit, arrival, delivery events | X12 214 Transportation Carrier Shipment Status Message |
| Freight invoice | Linehaul, fuel, accessorials such as detention | X12 210 Motor Carrier Freight Details and Invoice |
| Bill of lading | Contract of carriage and receipt for goods | X12 211 Motor Carrier Bill of Lading; paper or PDF in practice; for ocean, [DCSA](https://dcsa.org/standards) electronic bill of lading standards |
| Telematics, ELD, GPS pings | Position, speed, engine data, driver hours | Driver hours are limited by [49 CFR 395.3](https://www.law.cornell.edu/cfr/text/49/395.3): 11 hours driving within a 14-hour window, after 10 hours off duty |
| Appointment systems | Booked windows at pickup and delivery docks | |
| Rates | Contract rates per lane, spot quotes, fuel surcharge tables | |
| Proof of delivery | Signed delivery receipt, often a photo of paper | |

The common data problem: the same stop has three timestamps (the carrier's 214, the GPS geofence and the dock's gate log) and they disagree. Decide which one is the truth for each KPI before building models on any of them.

## Classical methods that work
| Method | Use it for | Reference |
|---|---|---|
| Vehicle routing solvers (hybrid genetic search, local search, guided local search) | Own-fleet and last-mile routing with capacities and time windows | [PyVRP](https://github.com/PyVRP/PyVRP), [OR-Tools routing](https://developers.google.com/optimization/routing) |
| MILP load building and consolidation | Combining orders into full truckloads or multi-stop loads | [Pyomo](https://github.com/Pyomo/pyomo), [PuLP](https://github.com/coin-or/pulp) |
| Routing guides with waterfall tendering | Carrier selection per load: primary first, then backups, then spot | Standard TMS practice |
| Bid optimization in procurement events | Lane awards across hundreds of carriers with capacity and diversity constraints | MILP |
| Routing-engine ETA plus a residual model | ETAs: start from the map's drive time, then learn the error from history | [DeeprETA](https://arxiv.org/abs/2206.02127) (*background*, 2022) |
| Quantile regression and conformal prediction | ETA intervals with a stated coverage | [A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511) (*background*, 2021), [MAPIE](https://github.com/scikit-learn-contrib/MAPIE) |
| Hours-of-service-aware planning | Feasible driver plans under the 11-hour and 14-hour rules | [49 CFR 395.3](https://www.law.cornell.edu/cfr/text/49/395.3) |

Standard instances: [CVRPLIB](https://vrp.galgos.inf.puc-rio.br/index.php/en/), Solomon VRPTW (see [datasets](../../datasets/README.md)).

## What fits
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Vehicle routing | Planning | Routing solvers (OR-Tools, PyVRP); learning-to-optimize methods as warm starts or decomposition | Neural routers on Euclidean toy instances sold as fleet-ready |
| Load building | Planning | MILP with real dimensions, weights and stop sequences | Rules of thumb that ignore cube |
| Carrier selection and tendering | Planning + prediction | Acceptance-probability models feeding a cost-aware routing guide | Always tendering to the cheapest carrier with the lowest acceptance |
| ETA prediction | Prediction | Gradient-boosted trees on lane, dwell and HOS features; conformal intervals on top | A single point ETA with no range; asking an LLM for the ETA |
| Rate and spot price prediction | Prediction | Time-series and tree models on lane history and market indices | Treating a forecast as a price commitment |
| Carrier follow-up, rebooking, appointment changes | Coordination | LLM agents with tools, an allowed-action list and approval on money | Agents that can accept rates or pay invoices on their own |
| Bills of lading, proof of delivery, invoices | Documents | Document AI or vision-language models plus validation rules (totals, weights, references matched to the TMS) | Extraction with nothing checking it |
| Freight audit | Documents + rules | Match the 210 invoice to the contract rate and the 214 events (for detention claims) | Paying accessorials no event supports |
| Shipment status across companies | Shared truth | EDI 214 and agreed event definitions first; a neutral visibility platform | Each party keeping its own version of the arrival time |

## AI in practice, 2025 to 2026
| Claim | Verdict | Evidence |
|---|---|---|
| "ML beats rule-based ETAs and delivery promises" | Yes, when the data is good, and calibrated intervals help most where it matters (late loads) | [Conformal predictive distributions for fulfilment time](https://arxiv.org/abs/2505.17340): up to 14% higher accuracy and up to 75% better at spotting late deliveries than the existing rule-based system, on one large industrial dataset. [Multi-task delay prediction](https://arxiv.org/abs/2602.20271): 0.67 to 0.91 days MAE on delayed shipments across 10 million records, 41% to 64% better than tree baselines |
| "LLMs can solve routing problems" | As code writers for heuristics, sometimes. As the router, no | [ARS / RoutBench](https://arxiv.org/abs/2502.15359): LLM agents write constraint-aware heuristic code and solve 91.67% of common variants in its benchmark. The plan still comes from an algorithm, not from text |
| "Neural routing replaces OR solvers" | Research progress on real road networks and constraints; not a replacement at fleet scale | [RRNCO](https://arxiv.org/abs/2503.16159), [constraint handling](https://arxiv.org/abs/2602.16012); [FrontierCO](https://arxiv.org/abs/2505.16952) finds learned solvers still trail classical ones on large instances |
| "Let LLM agents pick carriers" | Watch the market effects | [When Shippers Become Algorithms](https://arxiv.org/abs/2607.19967): in simulation, LLM shipper agents converged on the same carrier, which drew up to 76% of requests on day one; showing remaining carrier capacity cut concentration by a third |
| "Real-time bid acceptance with ML" | Solvable with simple policies plus rollouts; now has a public benchmark | [FreightBidBench](https://arxiv.org/abs/2607.07343): simple policies keep 86.5% to 91.0% of rollout profit on its scenarios |
| "Driverless trucks are here" | On selected highway lanes, yes; yards, gates and docks are not ready | Aurora began commercial driverless runs between Dallas and Houston in May 2025 ([TechCrunch](https://techcrunch.com/2025/05/01/aurora-launches-commercial-self-driving-truck-service-in-texas/)) |
| "Agents will fix detention" | They can attack the coordination part: appointments, early warnings, claims with evidence | No public controlled study yet. See the guardrails pattern in [06-agent-with-guardrails](../../implementations/06-agent-with-guardrails) |

## Worked example: what detention costs a shipper
*Illustrative numbers, except the detention rate, which is ATRI's 2023 survey figure used as an assumption.*

A shipper moves 200 loads a week, each with a pickup and a delivery: 400 stops.

| Step | Calculation | Result |
|---|---|---|
| Detained stops a week | 400 x 0.393 | 157.2 |
| Billable detention hours (1.5 h each beyond free time) | 157.2 x 1.5 | 235.8 h |
| Weekly cost at $75 an hour | 235.8 x 75 | $17,685 |
| Yearly cost (52 weeks) | 17,685 x 52 | $919,620 |
| Cut the detention rate by 5 points (20 fewer stops a week) | 20 x 1.5 x 75 x 52 | $117,000 a year |

What to notice:
- The 5-point cut does not need a better ETA model alone. It needs the ETA to reach the dock scheduler early enough to move an appointment, which is coordination.
- An ETA is only useful for this if its interval is honest. A 90% interval that holds 70% of arrivals sends the dock wrong signals. Check coverage, not just MAE: see [12-eta-calibration](../../implementations/12-eta-calibration).
- Detention claims need evidence. Matching 214 events and geofence times to the invoice turns a disputed charge into a paid or rejected one.

## Common mistakes
- Reporting ETA mean absolute error and never checking whether the stated range holds.
- Training ETA models on carrier 214 timestamps that were keyed in hours after the event.
- Optimizing cost per load and ignoring tender acceptance, so the "cheap" carrier rejects and the load goes to spot at a premium.
- Benchmarking a learned router on random Euclidean points, then deploying on roads with time windows, driver hours and docks that close.
- Building an agent that can accept rates or approve accessorials with no human approval on money.
- Extracting bills of lading with an LLM and loading the result straight into billing with no check against the order.
- Measuring detention from carrier invoices only. Invoices undercount it, since fleets are paid on fewer than half of detention invoices ([ATRI](https://truckingresearch.org/2024/09/new-research-documents-substantial-financial-and-safety-impacts-from-truck-driver-detention/)).

## Run it
- [12-eta-calibration](../../implementations/12-eta-calibration): calibrated ETA intervals with conformal prediction.
- [13-document-validation](../../implementations/13-document-validation): bill of lading extraction checked by validation rules.
- [04-llm-solver-interface](../../implementations/04-llm-solver-interface): an LLM translates a planner's question, a solver re-optimizes the lanes.
- [06-agent-with-guardrails](../../implementations/06-agent-with-guardrails): an agent chases a missing proof of delivery, with allowed actions and approvals.

## Key papers
Full list: [papers](../../papers/2025-2026.md#routing).

| Paper | Why read it |
|---|---|
| [RRNCO: Towards Real-World Routing with Neural Combinatorial Optimization](https://arxiv.org/abs/2503.16159) (2025) | Neural routing on real road networks instead of Euclidean toys |
| [Learning to Segment for Vehicle Routing Problems](https://arxiv.org/abs/2507.01037) (2025) | Learned decomposition for large instances |
| [Towards Efficient Constraint Handling in Neural Solvers for Routing Problems](https://arxiv.org/abs/2602.16012) (2026) | The constraints real fleets have |
| [Neural Cluster First, Route Second](https://arxiv.org/abs/2605.09301) (2026) | Recurring routes over the same service area |
| [Enhancing Cross-Problem Vehicle Routing via Federated Learning](https://arxiv.org/abs/2604.10652) (2026) | Sharing routing models across operators without sharing data |
| [ARS: Automatic Routing Solver with Large Language Models](https://arxiv.org/abs/2502.15359) (2025) | LLM agents writing constraint-aware routing heuristics; RoutBench with 1,000 variants |
| [Conformal Predictive Distributions for Order Fulfillment Time Forecasting](https://arxiv.org/abs/2505.17340) (2025) | Distribution-free intervals for delivery time, with a cost-aware decision rule |
| [Uncertainty-Aware Delivery Delay Duration Prediction via Multi-Task Deep Learning](https://arxiv.org/abs/2602.20271) (2026) | Rare but costly delays, 10 million shipments, conformal intervals |
| [Latency-Aware Bid Acceptance under Operational Feasibility](https://arxiv.org/abs/2607.07343) (2026) | FreightBidBench: a public truckload bid-acceptance benchmark with hours of service and yard delays |
| [When Shippers Become Algorithms](https://arxiv.org/abs/2607.19967) (2026) | What happens to a freight market when LLM agents pick carriers |
| [Coordinating Spot and Contract Supply in Freight Marketplaces](https://arxiv.org/abs/2603.24574) (2026) | Contract capacity and spot pricing optimized together |
| [Elephants or Goldfish? Carrier Reciprocity in Dynamic Freight Markets](https://arxiv.org/abs/2108.07348) (*background*, 2021) | Carriers respond to current shipper behaviour, not past loyalty: why tender acceptance swings with the market |
| [FrontierCO](https://arxiv.org/abs/2505.16952) (2025) | Learned solvers versus classical ones at real scale, routing included |

## Tools and datasets
| Tool or dataset | Use | Where |
|---|---|---|
| PyVRP, OR-Tools | Routing solvers | [Optimization and routing tools](../../repos/README.md#optimization-and-routing) |
| RL4CO | Learned routing baselines | [ai4co/rl4co](https://github.com/ai4co/rl4co) |
| MAPIE | Conformal prediction intervals in Python | [scikit-learn-contrib/MAPIE](https://github.com/scikit-learn-contrib/MAPIE) |
| Awesome conformal prediction | Reading list for intervals | [valeman/awesome-conformal-prediction](https://github.com/valeman/awesome-conformal-prediction) |
| CVRPLIB, Solomon | Routing benchmark instances | [datasets](../../datasets/README.md) |
| LaDe | Last-mile pickup and delivery records from Cainiao | [Hugging Face](https://huggingface.co/datasets/Cainiao-AI/LaDe) |
| Amazon Last Mile Routing Research Challenge | Real driver routes with sequences | [AWS Open Data](https://registry.opendata.aws/amazon-last-mile-challenges/) |
| Freight Analysis Framework (FAF5) | US freight flows by mode, origin and destination | [ORNL](https://faf.ornl.gov/faf5/) |
| DataCo, Olist | Orders with shipping and delivery times | [datasets](../../datasets/README.md) |
| Fleetbase | Open-source logistics operating system | [fleetbase/fleetbase](https://github.com/fleetbase/fleetbase) |

## Open problems
- Calibrated ETAs: accuracy is reported, the value of the error bar rarely is (see [open problems](../open-problems.md), #6).
- Driverless trucks arriving at yards and gates designed for a driver to talk to (#7). Highway lanes are running; the first and last hundred metres are not.
- Learned routing methods at real fleet scale with real constraints.
- **Ground truth for arrival.** Carrier events, GPS geofences and gate logs disagree. There is no shared definition of "arrived", so ETA models are trained and scored against different truths.
- **Market effects of agent procurement.** If many shippers delegate carrier choice to similar LLM agents, demand can pile onto the same carriers ([simulation evidence](https://arxiv.org/abs/2607.19967)). Platform rules that prevent this are untested in live markets.
- **Measuring detention without a survey.** The best public number is driver-reported. A neutral, event-based measure across shippers would let anyone test whether an intervention works.
- **Document checks at network scale.** Validation rules catch arithmetic and reference errors on one bill of lading. Catching a wrong consignee or weight across thousands of partners needs shared reference data that rarely exists.

## Further reading
- Paolo Toth and Daniele Vigo (eds.), *Vehicle Routing: Problems, Methods, and Applications*, 2nd ed., SIAM, 2014.
- MIT OpenCourseWare, [1.203J Logistical and Transportation Planning Methods](https://ocw.mit.edu/courses/1-203j-logistical-and-transportation-planning-methods-fall-2006/).
- MITx [MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM) (MIT Learn, free to audit).
- ASCM [CLTD certification](https://www.ascm.org/learning-development/certifications-credentials/cltd/) (logistics, transportation and distribution body of knowledge).
- [Google OR-Tools routing guide](https://developers.google.com/optimization/routing).
- Standards: [X12 transaction sets](https://x12.org/products/transaction-sets), [DCSA standards](https://dcsa.org/standards) (ocean), US hours of service at [49 CFR 395.3](https://www.law.cornell.edu/cfr/text/49/395.3).
- Research: [American Transportation Research Institute](https://truckingresearch.org/2024/09/new-research-documents-substantial-financial-and-safety-impacts-from-truck-driver-detention/) on detention and operating costs.
