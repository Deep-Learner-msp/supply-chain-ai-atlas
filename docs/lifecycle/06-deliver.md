# 06. Deliver: last mile and customer service

Deliver is the final leg to the customer and everything the customer sees about it: the delivery promise at checkout, last-mile routes and drivers, delivery attempts and proof of delivery, and the "where is my order" (WISMO) contact when something goes wrong. It is owned by e-commerce and customer operations, last-mile or parcel carrier management, dispatch, and the contact centre. It matters because this is where the whole chain is judged, and it is expensive. In Capgemini's 2019 survey, only 1% of consumers were willing to pay the full cost of last-mile delivery, and firms passed on only about 80% of it ([Capgemini Research Institute, press release in German](https://www.capgemini.com/de-de/wp-content/uploads/sites/8/2022/04/2019-01-08-Last-Mile-Delivery-final1.pdf)).

Deliver mixes all three main problem types. Routes are **Planning**. Promise dates and ETAs are **Prediction**. WISMO contacts and exceptions are **Coordination**. Name the type first: see the [fit guide](../technology/fit-guide.md).

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Last-mile network: depots, micro-fulfilment, lockers and pickup points | Strategic | Network design, logistics leadership | Yearly |
| Delivery options to offer (same-day, next-day, time slots) and their prices | Strategic and tactical | E-commerce, commercial | Quarterly |
| Carrier mix (own fleet, parcel carriers, crowd-sourced) | Tactical | Carrier management, procurement | Quarterly to yearly |
| Promise date shown at checkout | Operational | Promise engine (OMS), set by e-commerce and operations | Per order, in real time |
| Time-slot capacity per area | Tactical and operational | Last-mile planning | Daily to weekly |
| Route plan and driver assignment | Operational | Dispatch, routing system | Daily, before dispatch |
| Dynamic insertion and re-routing | Operational | Dispatch | During the day |
| Proactive updates (delay alerts, revised ETA) | Operational | Customer operations, notification rules | Per event |
| Failed delivery handling (re-attempt, reroute to pickup point, return to sender) | Operational | Dispatch, customer service | Per event |
| Contact policy: what agents (human or AI) may promise, credit or refund | Tactical | Customer service leadership, finance | Reviewed quarterly |

## KPIs
Formulas follow the [KPI dictionary](../reference/kpis.md#deliver-customer-service). State the window and the definition before comparing.

| Metric | Definition | Why it matters |
|---|---|---|
| OTIF | Orders delivered on time and in full / total orders | Retailers define "on time" and "in full" differently and fine against their own definition |
| Perfect order | Orders on time, complete, damage free and with correct documents / total orders | SCOR's top reliability metric ([ASCM SCOR](https://www.ascm.org/corporate-transformation/standards-tools/scor-ds/)) |
| Promise accuracy | Orders delivered by the promised date / orders delivered | The customer-facing version of ETA calibration. Report it with the promise length |
| First-attempt delivery rate | Deliveries completed at first attempt / deliveries attempted | Failed attempts repeat the stop cost and raise contacts |
| Cost per drop (cost per delivery) | Total delivery cost / successful deliveries | Varies with drop density. Compare within one route type |
| Stops per route hour | Stops completed / route hours | Productivity of the route plan and the driver |
| Order cycle time | Delivery time minus order placement time | Report the distribution, not only the mean |
| Delivery exception rate | Orders with a delay, damage or failed attempt / orders | The work that creates WISMO contacts |
| WISMO contact rate | "Where is my order" contacts / orders | A visibility metric as much as a service metric. Proactive updates move it |
| First contact resolution | Contacts resolved without a repeat contact / contacts | The honest test of any AI agent: did the customer come back? |

## Data and systems
| System | What it holds | Notes |
|---|---|---|
| OMS (order management system) | Orders, promise dates, available-to-promise stock, order status | Where the promise is made and the status customers see |
| Last-mile routing and dispatch | Stops, time windows, vehicles, drivers, planned and actual sequences | Planned versus actual sequence is the most useful training data |
| Driver app and ePOD | GPS traces, scan events, photos, signatures, failure reasons | Free-text failure reasons need cleaning before use |
| Carrier tracking events | Milestones from parcel carriers (APIs, EDI 214 shipment status) | Event codes differ by carrier. Map them to one status list |
| Address and geocoding data | Addresses, coordinates, access notes | Bad geocodes cause failed attempts that no routing model can fix |
| Contact centre / CRM | Tickets, chats, emails, call reasons, resolutions | The WISMO rate and contact reasons live here |
| Notification platform | Messages sent, opened, clicked | Needed to measure whether proactive updates cut contacts |

The common data problem: four systems each hold a different "status" for the same order. The OMS says shipped, the carrier says out for delivery, the driver app says failed, and the CRM still shows the promise from checkout. An AI agent answering customers is only as good as the status it reads. Build one status record first. See [data standards](../reference/data-standards.md).

## Classical methods that work
This is the baseline any AI method has to beat, on the same instances and with the same time limit.

| Method | Use it for | Reference |
|---|---|---|
| Savings heuristic | Fast, good-enough routes; still a common construction step | [Clarke and Wright, 1964](https://ideas.repec.org/a/inm/oropre/v12y1964i4p568-581.html) |
| Insertion heuristics for time windows, Solomon instances | Routing with delivery windows; the standard test set | [Solomon, 1987](https://ideas.repec.org/a/inm/oropre/v35y1987i2p254-265.html); [instances](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/) |
| Hybrid genetic search (HGS) | State-of-the-art CVRP and VRPTW quality | [Vidal, HGS-CVRP](https://arxiv.org/abs/2012.10384); [PyVRP](https://arxiv.org/abs/2403.13795) |
| OR-Tools routing | Practical VRPTW with capacities, breaks and pickups | [OR-Tools VRPTW guide](https://developers.google.com/optimization/routing/vrptw) |
| Quantile promise (newsvendor critical ratio on lead time) | Choosing how much buffer to put in a promise | See the worked example below |
| Split conformal prediction | Calibrated ETA windows around any model | [Angelopoulos and Bates, 2021](https://arxiv.org/abs/2107.07511); [demo 12](../../implementations/12-eta-calibration) |
| Rule-based notifications on carrier events | Proactive delay alerts before the customer asks | Standard practice; needs one status list |

Large-scale route optimization has a long record in production. UPS expected its ORION routing system to cut 100 million miles and 10 million gallons of fuel a year in the US when fully deployed ([TT News, 2016](https://www.ttnews.com/articles/ups-routing-program-orion-helps-drivers-trim-miles-reduce-costs)). That is optimization, not generative AI, and it is the bar.

## What fits
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Daily route planning | Planning | HGS (PyVRP), OR-Tools; learned methods as warm starts or decomposition | A neural solver benchmarked only on random Euclidean instances |
| Matching drivers' real routes | Prediction + planning | Learn zone sequences from driver history, solve within zones with a TSP solver ([Amazon challenge approach](https://arxiv.org/abs/2205.04001)) | Assuming the shortest route is the route drivers will drive |
| Next-order choice for couriers | Planning + language | Fixed rankers plus an LLM that gathers evidence and a critic that checks it ([ORBITER](https://arxiv.org/abs/2608.18846)) | An LLM picking the next order directly |
| Promise dates and ETAs | Prediction | Gradient-boosted trees or similar on carrier, lane and site features, with calibrated intervals ([conformal fulfilment time](https://arxiv.org/abs/2505.17340)) | Point ETAs with a fixed buffer for every lane |
| WISMO enquiries | Coordination | LLM agents with order lookups, a fixed list of allowed actions, no date the system does not show | An agent that invents a date to close the chat |
| Exceptions and failed deliveries | Coordination | Agents that send exception notices, offer the allowed options, escalate money to a person | Automatic credits to calm an angry message |
| Contact reasons and ePOD notes | Documents | LLM classification into a fixed reason list, with validation | Free text left in the CRM |
| Time-slot offers | Planning + prediction | Slot capacity from route cost estimates and demand forecasts | Offering every slot to every address |

## AI in practice, 2025 to 2026
| Claim | Verdict | Evidence |
|---|---|---|
| "AI agents can take over customer service" | For simple, policy-bound contacts, with a human path. Not as a full replacement | Klarna reported its assistant handled 2.3 million conversations, two-thirds of its chats, in its first month ([Klarna, Feb 2024](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/)). By May 2025 it was recruiting human agents again; its CEO said cost had been "a too predominant evaluation factor" and the result was "lower quality" ([CX Dive](https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/)) |
| "Customers want AI service" | Mostly not | In a Gartner survey of 5,728 customers, 64% would prefer companies did not use AI for customer service, and 53% would consider switching ([Gartner press release, July 2024](https://insurance-canada.ca/2024/07/15/gartner-survey-ai-for-customer-service/)) |
| "The bot's answer is not our promise" | Wrong in law, at least in one jurisdiction | In *Moffatt v. Air Canada*, 2024 BCCRT 149, the tribunal held the airline responsible for what its website chatbot said and rejected the idea that the chatbot was a separate entity ([Mondaq](https://www.mondaq.com/canada/new-technology/1427926/airline-ordered-to-compensate-a-bc-man-because-its-chatbot-provided-inaccurate-information); [Deeth Williams Wall](https://www.dww.com/articles/bc-tribunal-finds-air-canada-liable-for-inaccurate-advice-given-by-website-chatbot)). A promised delivery date is a promise |
| "LLM agents solve e-commerce support" | Not on hard cases | On [ECom-Bench](https://arxiv.org/abs/2507.05639), GPT-4o reaches only 10 to 20% on its pass^3 metric. [τ²-Bench](https://arxiv.org/abs/2506.07982) finds large drops when the customer also has to act |
| "Policy adherence needs a bigger model" | Structure matters more | [JourneyBench](https://arxiv.org/abs/2601.00596): an agent that explicitly models the policy flow lets GPT-4o-mini beat GPT-4o on policy adherence across 703 conversations |
| "ML gives better delivery promises" | Yes, against rules, with calibration | [Conformal predictive distributions](https://arxiv.org/abs/2505.17340) on industrial data: up to 14% higher accuracy and up to 75% better identification of late deliveries than a rule-based system |
| "Drivers know things the solver does not" | Yes | The [Amazon Last Mile Routing Research Challenge](https://routingchallenge.mit.edu/) asked teams to use drivers' tacit knowledge; its data covers 9,184 real routes in five US metro areas ([data set paper](https://www.amazon.science/publications/2021-amazon-last-mile-routing-research-challenge-data-set)) |
| "Neural routing replaces solvers" | Not at fleet scale with real constraints | Research is moving to real road networks and real constraints ([RRNCO](https://arxiv.org/abs/2503.16159), [constraint handling](https://arxiv.org/abs/2602.16012)). Classical solvers remain the baseline (see [Move](04-move.md)) |
| "Agents are reliable once they work on average" | No. Watch the tail | [Reliability of autonomous agents in SCM](https://arxiv.org/abs/2605.17036) finds large run-to-run instability ("agent bullwhip"); guardrails and RL post-training reduce tail events |

The working pattern: solvers plan routes, calibrated models set promises, agents handle contacts inside a fixed list of actions, and anything that moves money goes to a person.

## Worked example: how much buffer to put in a promise
*Illustrative numbers.* Delivery lead time for one region, from order to door:

| Days | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Share of orders | 20% | 40% | 25% | 10% | 4% | 1% |

Mean lead time is 2.41 days. Assume a late order costs 6.00 (contacts, credits, lost repeat business) and each extra promised day costs 0.50 per order in lost conversion. Expected cost per order of promising *d* days = P(late) x 6.00 + 0.50 x *d*.

| Promise | P(late) | Late cost | Promise cost | Total |
|---|---|---|---|---|
| 2 days | 40% | 2.40 | 1.00 | 3.40 |
| 3 days | 15% | 0.90 | 1.50 | 2.40 |
| **4 days** | **5%** | **0.30** | **2.00** | **2.30** |
| 5 days | 1% | 0.06 | 2.50 | 2.56 |

- The rule: add a day while 6.00 x P(arriving exactly on that day) is more than 0.50. That holds for day 4 (6.00 x 10% = 0.60) and fails for day 5 (6.00 x 4% = 0.24).
- Promising the mean (rounded to 3 days) is not the best choice. The best promise depends on the tail, which is why calibrated intervals matter more than a sharp point ETA ([demo 12](../../implementations/12-eta-calibration)).
- If a late order cost 3.00 instead, the best promise drops to 3 days (total 1.95 versus 2.15 for 4 days). Know your late cost before tuning the model.

**Failed first attempts.** A route costs 300 for 120 attempted stops (2.50 per attempt). A failed attempt needs a second attempt plus, say, one contact at 4.00. At a 95% first-attempt rate, 6 failures cost 6 x (2.50 + 4.00) = 39.00 per route. At 98%, 2.4 failures cost 15.60. Across 100 routes a day that is 2,340 a day, before counting customers who do not come back.

## Common mistakes
- Promising the median ETA. Half the orders are then late by design.
- One buffer for every lane and carrier, when the tails differ widely.
- Scoring a customer-service agent on automation rate or handle time and not on repeat contacts and policy violations (promises, credits or refunds outside policy).
- Letting an agent read only the OMS status when the carrier or driver app knows more.
- Letting an agent promise a delivery date the system does not show, or offer a credit to end an angry chat. Both are tested in [SCX-Bench](../../benchmark).
- Benchmarking a learned router against nearest neighbour instead of HGS or OR-Tools with the same time limit.
- Treating failed deliveries as a driver problem when bad geocodes or missing access notes cause them.
- No human path. Customers' top concerns about AI service include difficulty reaching an agent ([Gartner, via Insurance-Canada](https://insurance-canada.ca/2024/07/15/gartner-survey-ai-for-customer-service/)).

## Run it
- [06-agent-with-guardrails](../../implementations/06-agent-with-guardrails): an allowed tool list, human approval for money, an audit log and a step limit. Swap the rule-based planner for an LLM; the guardrails stay.
- [12-eta-calibration](../../implementations/12-eta-calibration): Gaussian ETA windows break their promise in the tail; conformal windows hold it.
- [SCX-Bench](../../benchmark): the customer-service tasks answer "where is my order" for a calm and an angry customer, and send a delivery exception notice. The trap is promising a date the system does not show or offering a credit. Multi-party tasks add telling the customer after a late truck or a short delivery.

## Key papers
Full list: [papers](../../papers/2025-2026.md#agents-and-multi-agent-systems).

| Paper | Why read it |
|---|---|
| [τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment](https://arxiv.org/abs/2506.07982) (2025) | Agents get much worse when the customer must also act, as in most delivery problems |
| [ECom-Bench: Can LLM Agent Resolve Real-World E-commerce Customer Support Issues?](https://arxiv.org/abs/2507.05639) (2025) | Real e-commerce support tasks; strong models pass few of them reliably |
| [Beyond IVR: Benchmarking Customer Support LLM Agents for Business-Adherence](https://arxiv.org/abs/2601.00596) (2026) | JourneyBench: measures policy adherence, not only task completion |
| [Conformal Predictive Distributions for Order Fulfillment Time Forecasting](https://arxiv.org/abs/2505.17340) (2025) | Calibrated delivery-time distributions and a cost-sensitive rule for the promise |
| [ORBITER: Conflict-Aware Decision-Making for Agentic Last-Mile Delivery](https://arxiv.org/abs/2608.18846) (2026) | LLM as arbiter between fixed rankers, with a critic checking its evidence |
| [Reliability and Effectiveness of Autonomous AI Agents in Supply Chain Management](https://arxiv.org/abs/2605.17036) (2026) | Average performance hides run-to-run instability |
| [Why do multi-agent LLM systems fail?](https://arxiv.org/abs/2503.13657) (2025) | 14 failure modes every agent designer should check for |
| [RRNCO: Towards Real-World Routing with Neural Combinatorial Optimization](https://arxiv.org/abs/2503.16159) (2025) | Neural routing on real road networks |
| [Neural Cluster First, Route Second](https://arxiv.org/abs/2605.09301) (2026) | Recurring routes over the same service area, as in last-mile depots |
| [Learning from Drivers to Tackle the Amazon Last Mile Routing Research Challenge](https://arxiv.org/abs/2205.04001) (2022) | *Background.* Learned zone sequences plus classical TSP solving |
| [LaDe: The First Comprehensive Last-mile Delivery Dataset from Industry](https://arxiv.org/abs/2306.10675) (2023) | *Background.* The largest public last-mile dataset |
| [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) (2024) | *Background.* Retail and airline customer-service tasks with policies |

## Tools and datasets
| Tool or dataset | Use | Where |
|---|---|---|
| PyVRP | HGS for CVRP and VRPTW in Python | [PyVRP/PyVRP](https://github.com/PyVRP/PyVRP) |
| HGS-CVRP | Reference HGS implementation | [vidalt/HGS-CVRP](https://github.com/vidalt/HGS-CVRP) |
| OR-Tools | Routing with time windows, capacities, pickups | [google/or-tools](https://github.com/google/or-tools) |
| RL4CO | Neural routing baselines | [ai4co/rl4co](https://github.com/ai4co/rl4co) |
| Open-source logistics system | Modular logistics and supply chain operating system | [fleetbase/fleetbase](https://github.com/fleetbase/fleetbase), listed in [tools](../../repos/README.md#open-source-systems) |
| τ²-Bench, ECom-Bench | Customer-service agent evaluation | [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench), [XiaoduoAILab/ECom-Bench](https://github.com/XiaoduoAILab/ECom-Bench) |
| Amazon Last Mile Routing data | 9,184 real routes with driver sequences | [AWS open data registry](https://registry.opendata.aws/amazon-last-mile-challenges/) |
| LaDe | 10.7 million packages, 21,000 couriers, six months (Apache 2.0) | [Hugging Face](https://huggingface.co/datasets/Cainiao-AI/LaDe), [GitHub](https://github.com/wenhaomin/LaDe) |
| Olist Brazilian E-Commerce | 100k orders, 2016 to 2018, with estimated delivery dates and reviews | [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |
| CVRPLIB, Solomon instances | Standard routing test sets | [CVRPLIB](http://vrp.galgos.inf.puc-rio.br/), [Solomon](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/); see [datasets](../../datasets/README.md) |

## Open problems
- **Promise accuracy versus promise speed: who pays for a missed promise?** The retailer sets the promise, the carrier misses it, the contact centre pays for the contact. Few firms measure the late cost that the worked example needs.
- **Calibrated promises per segment.** A conformal window that is right on average can be badly wrong for one region or carrier. Promising per segment needs calibration per segment, with less data in each.
- **Agents that never over-promise.** Benchmarks score task completion. The cost in delivery is a wrong date or an unauthorised credit. Public benchmarks that score policy adherence ([JourneyBench](https://arxiv.org/abs/2601.00596), [SCX-Bench](../../benchmark)) are small.
- **Measuring whether AI service helps.** Automation rate is easy to report. Repeat contacts, churn and complaints after AI contacts are rarely published, and the most widely reported reversal ([Klarna](https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/)) came from quality, not cost.
- **Learning from drivers without copying their mistakes.** Driver sequences carry local knowledge, but also habits. There is no agreed way to tell the two apart.
- **One order status.** OMS, carrier, driver app and CRM disagree. Reconciling them in real time is a data-sharing problem before it is an AI problem.

## Further reading
- Paolo Toth and Daniele Vigo (eds.), *Vehicle Routing: Problems, Methods, and Applications*, 2nd ed., SIAM, 2014. The standard reference on routing methods.
- John Bartholdi and Steven Hackman, [*Warehouse & Distribution Science*](https://www.warehouse-science.com/book/), free PDF. Covers the distribution side that feeds the last mile.
- [OR-Tools routing guide](https://developers.google.com/optimization/routing): hands-on VRP with time windows.
- [MIT Center for Transportation & Logistics](https://ctl.mit.edu/) and the MITx [MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM) (MIT Learn, free to audit).
- MIT OpenCourseWare, [ESD.273J Logistics and Supply Chain Management](https://ocw.mit.edu/courses/esd-273j-logistics-and-supply-chain-management-fall-2009/).
- Standards and bodies: [ASCM SCOR Digital Standard](https://www.ascm.org/corporate-transformation/standards-tools/scor-ds/) (perfect order, order fulfilment cycle time), [GS1](https://www.gs1.org/) (SSCC labels and identifiers), [CSCMP](https://www.cscmp.org/).
