# 05. Store: warehouse, yard and dock

Store is everything between the truck arriving at the gate and the order leaving on another truck: yard, dock, receiving, put-away, storage, picking, packing and shipping. It is owned by site general managers, warehouse operations and engineering, inventory control, and (more and more) a robotics or automation team. It matters because it is labour-heavy and close to the customer. Order picking alone is estimated at up to 55% of warehouse operating cost ([de Koster, Le-Duc and Roodbergen, 2007](https://doi.org/10.1016/j.ejor.2006.07.009)), and a slow or wrong pick shows up downstream as a late or wrong delivery in [Deliver](06-deliver.md).

Most of Store is **Planning** (slotting, dock schedules, batching, robot task assignment) fed by **Prediction** (inbound volume, labour hours, dwell). The yard and dock add **Coordination** with carriers. Name the type first: see the [fit guide](../technology/fit-guide.md).

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Site location, size and automation level (manual, AMR, AS/RS, goods-to-person) | Strategic | Network design, operations leadership | Every few years |
| Layout: zones, aisles, forward pick area, dock count | Strategic | Industrial engineering | At design, then on major change |
| Storage policy (random, class-based, dedicated) and slotting | Tactical | Inventory control, engineering | Quarterly re-slot, weekly moves for fast movers |
| Dock appointment rules and door assignment | Tactical and operational | Transport and receiving leads | Daily, plus on late trucks |
| Yard moves: which trailer to which door, when | Operational | Yard lead, YMS | Continuous |
| Labour plan: headcount, shifts, overtime, temps | Tactical | Site GM, workforce planning | Weekly, revised daily |
| Wave or waveless release, order batching, picker and robot task assignment | Operational | WMS, WES, shift lead | Minutes to hours |
| Replenishment of pick faces | Operational | Inventory control | Per shift or on trigger |
| Cycle counting programme | Tactical | Inventory control | Daily counts, ABC-driven frequency |

## KPIs
Formulas follow the [KPI dictionary](../reference/kpis.md#store-warehouse-and-yard). These are standard definitions; always state which version you report.

| Metric | Definition | Why it matters |
|---|---|---|
| Dock-to-stock time | Put-away confirmed time minus receipt at dock time | Stock is not sellable until put away. Long dock-to-stock looks like a supplier delay to the planner |
| Dock door utilization | Door hours occupied by a trailer / door hours available | Low with long yard queues means a scheduling problem, not a capacity problem |
| Yard dwell | Gate-out time minus gate-in time, per trailer | Drives detention charges (see [Move](04-move.md)) |
| Pick rate | Lines (or units) picked / labour hours | Lines and units give very different numbers. Compare like-for-like order profiles only |
| Picking accuracy | Orders picked without error / orders picked | Errors found by the customer cost far more than errors caught at pack-out |
| Order cycle time (in the DC) | Ship confirm time minus order release time | What the customer cut-off depends on |
| On-time shipment | Orders shipped by the planned ship time / orders due to ship | One of the five most used metrics in WERC's 2025 DC Measures report ([MHI Solutions](https://www.mhisolutionsmag.com/index.php/2025/09/18/werc-releases-2025-dc-measures-report-with-a-focus-on-combining-vision-with-vigilance/)) |
| Inventory record accuracy | Locations where the system quantity matches the count within tolerance / locations counted | Every planning and AI model trusts the system number. This caps their quality |
| Storage (space) utilization | Occupied locations (or cube) / total | Above roughly 85 to 90%, travel and re-handling rise sharply |
| Cost per unit shipped | Total site operating cost / units shipped | The number finance compares across sites |

WERC's 2025 report tracks more than 30 metrics; its five most used were on-time shipments, average and peak capacity used, order-picking accuracy and dock-to-stock cycle time ([MHI Solutions](https://www.mhisolutionsmag.com/index.php/2025/09/18/werc-releases-2025-dc-measures-report-with-a-focus-on-combining-vision-with-vigilance/)).

## Data and systems
| System | What it holds | Notes |
|---|---|---|
| WMS (warehouse management system) | Locations, inventory by location, tasks, receipts, picks, shipments | The system of record. Most AI work starts with its task history |
| WES / WCS (execution and control systems) | Real-time release of work to people, conveyors, sorters and robots | Where waveless picking and machine control happen |
| YMS (yard management system) | Gate events, trailer locations, door assignments, appointments | Often a spreadsheet or the WMS dock module at smaller sites |
| Dock appointment scheduling | Carrier bookings, time slots, door rules | Feeds detention and on-time metrics |
| Slotting tool | SKU dimensions, velocity, affinity, location attributes | Can be a module of the WMS or a separate optimizer |
| Robot fleet manager | Robot positions, tasks, charging, traffic | Vendor-specific; rarely exposes clean data to the WMS |
| LMS (labour management system) | Engineered labour standards, actual time per task, performance by person | Needed for any labour forecast |
| ERP, OMS | Purchase orders, sales orders, ASNs (EDI 856, DESADV) | The ASN is the best early signal of inbound work. See [data standards](../reference/data-standards.md) |

Identifiers: pallets and cases carry a GS1 [SSCC](https://www.gs1.org/standards/id-keys/sscc) on the label, which links the physical unit to the ASN. Without it, receiving is manual keying and dock-to-stock grows.

The common data problem: the WMS knows where stock *should* be, not where it is. If inventory record accuracy is 95% by location, one pick in twenty may send someone to a wrong or empty slot. Fix counts and location master data before training anything on them.

## Classical methods that work
This is the baseline any AI method has to beat, on the same layout and order profile.

| Method | Use it for | Reference |
|---|---|---|
| ABC or class-based storage by pick frequency (or cube-per-order index) | Putting fast movers near the dock or pick-and-drop point | [Hausman, Schwarz and Graves, 1976](https://ideas.repec.org/a/inm/ormnsc/v22y1976i6p629-638.html); [Bartholdi and Hackman](https://www.warehouse-science.com/book/), slotting chapters |
| Picker routing heuristics (S-shape, return, largest gap) and the exact method for single-block layouts | Shorter pick tours without new hardware | [Ratliff and Rosenthal, 1983](https://ideas.repec.org/a/inm/oropre/v31y1983i3p507-521.html); [de Koster et al., 2007](https://doi.org/10.1016/j.ejor.2006.07.009) |
| Order batching (seed and savings heuristics), zoning, wave planning | Fewer tours per order | [de Koster et al., 2007](https://doi.org/10.1016/j.ejor.2006.07.009) |
| Engineered labour standards and workload-based staffing (forecast volume / standard rate) | Headcount per shift and per process | [Bartholdi and Hackman](https://www.warehouse-science.com/book/) |
| CP or MILP dock scheduling with a stability penalty | Door and slot assignment, re-planning for late trucks | [05-dock-scheduling](../../implementations/05-dock-scheduling); [OR-Tools](https://github.com/google/or-tools) |
| Queueing and Little's law (WIP = throughput x time) | Sizing docks, staging lanes and buffers | [Bartholdi and Hackman](https://www.warehouse-science.com/book/) |
| ABC cycle counting | Keeping record accuracy high without a full stock take | Standard inventory control practice |

## What fits
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Dock appointments and door assignment | Planning | CP-SAT or MILP, ETA-aware re-planning with a penalty for moving trucks | A fresh "optimal" plan that moves seven trucks for 20 minutes saved ([demo 05](../../implementations/05-dock-scheduling)) |
| Carrier messages about late trucks | Coordination | An agent that reads the message, calls the scheduler, books inside the rules | An agent that books slots the truck cannot make |
| Slotting | Planning | Class-based storage plus optimization on frequency and affinity; learned demand as an input | Re-slotting so often that labour for moves eats the travel saving |
| Picker routing and batching | Planning | Routing heuristics, batching heuristics, CP or MILP for small waves | Deep RL with no comparison to largest-gap or a solver |
| Robot task assignment and traffic | Planning | Fleet-level optimization; learned traffic models where data is large | Treating order scheduling and path finding as separate problems ([WareRover](https://arxiv.org/abs/2602.13999)) |
| Labour planning | Prediction + planning | Volume forecasts (ASNs, orders) feeding shift optimization with engineered standards | A headcount model with no standards and no LMS data |
| Inbound volume and dwell | Prediction | Gradient-boosted trees on ASN, carrier and appointment features | Forecasting with no link to the dock schedule |
| Inventory counts, damage, label reading | Documents/vision | Computer vision with a human check on exceptions | Fully automated adjustments to stock with no review |
| "Why is the site slow today?" | Planning + language | An LLM agent querying WMS and simulation data through fixed queries ([KG + LLM](https://arxiv.org/abs/2507.17273)) | An LLM answering from memory with no data behind it |

## AI in practice, 2025 to 2026
| Claim | Verdict | Evidence |
|---|---|---|
| "Mobile robots are mainstream in large fulfilment" | Yes, at the largest operators | Amazon reported its one millionth robot in 2025 ([Amazon](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)). Before that, 750,000 robots helped complete 75% of its customer orders ([Fortune, May 2025](https://fortune.com/2025/05/07/amazon-robot-sense-of-touch/)) |
| "Foundation models coordinate robot fleets" | Early but real at one operator | DeepFleet is trained on movement data from hundreds of thousands of robots ([arXiv 2508.08574](https://arxiv.org/abs/2508.08574)). Amazon says it improves fleet travel efficiency by 10% ([Amazon Science](https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination)). This is the operator's own figure, not an independent audit |
| "Learned methods beat rules for robot order allocation" | Promising in industrial data, not yet broadly replicated | [SOAR](https://arxiv.org/abs/2605.03842) reports a 7.5% makespan reduction on synthetic and real data with Geekplus. [OLSF-TRS](https://arxiv.org/abs/2605.08758) reports 8 to 12% fewer tote movements than heuristic baselines |
| "Robots can unload trailers" | Working for cases, at scale at some 3PLs | DHL reports Stretch unloading up to 700 cases per hour and signed a memorandum of understanding for 1,000+ more units in May 2025 ([Boston Dynamics](https://bostondynamics.com/news/dhl-signs-mou-for-additional-1000-robot-deployment/)). Vendor and customer figures |
| "Robots now pick any item" | Not yet | Amazon's Vulcan, its first robot with touch sensing, entered one site in 2025 with wider rollout planned from 2026 ([Fortune](https://fortune.com/2025/05/07/amazon-robot-sense-of-touch/)) |
| "Deep RL improves picking and charging" | In simulation | [DRL for AMR battery management](https://arxiv.org/abs/2607.05683) reports up to 6% higher order completion than the strongest baseline, in simulated multi-block warehouses |
| "AI forecasts labour needs" | Plausible, thinly evidenced | Workload forecasting is standard practice. We found no independent, peer-reviewed 2025 to 2026 evaluation on live sites to cite; most claims are vendor case studies |
| "LLM agents run the warehouse" | No. Useful as an analyst over data | [KG + LLM bottleneck analysis](https://arxiv.org/abs/2507.17273) works on simulation output with generated graph queries. Execution stays with the WMS, WES and solvers |
| "Computer vision keeps inventory accurate" | Useful for exceptions; no independent numbers | We list no accuracy figures because we found no independent evaluation to cite |

The pattern: robots and solvers execute, learned models predict traffic and volume, LLMs explain and coordinate. Gains reported by the operators themselves are real signals but not benchmarks.

## Worked example: ABC slotting and travel
*Illustrative numbers, simplified model.* A forward pick area has locations from 0 to 100 m from the pick-and-drop point. Each pick is a single trip out and back. 20% of SKUs (A) get 80% of picks, the next 30% (B) get 15%, the last 50% (C) get 5%.

| Storage policy | Average one-way distance per pick | Round-trip km for 2,000 picks | Walking hours at 1 m/s |
|---|---|---|---|
| Random (any SKU anywhere) | 50 m | 200 km | 55.6 h |
| Class-based (A in the nearest 20% of space, then B, then C) | 0.80 x 10 + 0.15 x 35 + 0.05 x 75 = 17 m | 68 km | 18.9 h |

- Travel falls by 66% (17 m versus 50 m).
- Travel is typically about half of a picker's time ([de Koster et al., 2007](https://doi.org/10.1016/j.ejor.2006.07.009), citing Tompkins et al.). So total picking time falls by about a third, not two thirds.
- Real tours pick several lines per trip, which dilutes the saving. The skew of demand matters most: with flat demand, class-based storage saves little.

What to notice:
- This is the baseline. A learned slotting method has to beat class-based storage plus a good routing heuristic, after counting the labour for the moves it asks for.
- Demand forecasts help when velocity shifts (seasonal items). That is where prediction feeds the plan.

## Common mistakes
- Reporting pick rate in units for one site and lines for another, then comparing them.
- Training models on WMS task data without checking inventory record accuracy first.
- Re-planning the dock from scratch for every late truck. Penalise moves ([demo 05](../../implementations/05-dock-scheduling)).
- Comparing a learned slotting or routing method against random storage instead of class-based storage with largest-gap routing.
- Re-slotting continuously and ignoring the labour and disruption of moving stock.
- Buying robots for peak volume and then planning labour as if robots never stop (charging, faults, maintenance).
- Treating yard, dock and inside operations as separate plans. A full dock and an empty pick floor is a scheduling failure.
- Letting an agent change stock records or book doors with no rule check and no audit trail.

## Run it
- [05-dock-scheduling](../../implementations/05-dock-scheduling): ten trucks, three doors, CP-SAT. A stable re-plan moves one truck; the "optimal" one moves seven.
- [SCX-Bench](../../benchmark): the dock and yard tasks ask an agent to move an appointment for a late truck, leave one that still fits, pick the right cross-dock outbound truck, and quarantine or release a reefer load after checking the temperature log. Each has a trap.

## Key papers
Full list: [papers](../../papers/2025-2026.md#warehouse-and-robotics).

| Paper | Why read it |
|---|---|
| [SOAR: Real-Time Joint Optimization of Order Allocation and Robot Scheduling in Robotic Mobile Fulfillment Systems](https://arxiv.org/abs/2605.03842) (2026) | Orders and robots planned together with deep RL, tested on industrial data |
| [DeepFleet: Multi-Agent Foundation Models for Mobile Robots](https://arxiv.org/abs/2508.08574) (2025) | Foundation models trained on a real fleet of hundreds of thousands of robots; compares four architectures |
| [It Takes Two to Tango: A Holistic Simulator for Joint Order Scheduling and Multi-Agent Path Finding in Robotic Warehouses](https://arxiv.org/abs/2602.13999) (2026) | WareRover: state-of-the-art methods falter when scheduling and path finding are coupled |
| [Dynamic Haven Selection for Multi-Agent Pickup and Delivery in Constrained Warehouses](https://arxiv.org/abs/2608.26939) (2026) | Robot pickup and delivery in single-width aisles, with completeness proofs |
| [Omni-scale Learning-based Sequential Decision Framework for Order Fulfillment of Tote-handling Robotic Systems](https://arxiv.org/abs/2605.08758) (2026) | Optimization plus multi-agent RL for order, tote and robot decisions |
| [Deep Reinforcement Learning for Dynamic Battery Management of Autonomous Order Pickers](https://arxiv.org/abs/2607.05683) (2026) | Charging is capacity: when and where robots charge |
| [Leveraging Knowledge Graphs and LLM Reasoning to Identify Operational Bottlenecks for Warehouse Planning Assistance](https://arxiv.org/abs/2507.17273) (2025) | LLM agents querying a knowledge graph of simulation output |
| [Integrated trucks assignment and scheduling problem with mixed service mode docks](https://arxiv.org/abs/2412.09090) (2024) | *Background.* Learning inside a dock-scheduling metaheuristic (Q-learning ALNS) |
| [Robotic warehousing operations: a learn-then-optimize approach to large-scale neighborhood search](https://arxiv.org/abs/2408.16890) (2024) | *Background.* Learning inside optimization |
| [Design and control of warehouse order picking: A literature review](https://doi.org/10.1016/j.ejor.2006.07.009) (2007) | *Background.* The map of storage, routing, batching and zoning problems |

## Tools and datasets
| Tool or dataset | Use | Where |
|---|---|---|
| OR-Tools CP-SAT | Dock and labour scheduling | [google/or-tools](https://github.com/google/or-tools), [CP-SAT primer](https://github.com/d-krupke/cpsat-primer) |
| Picking route and batching tutorials | Order batching and picker routes in Python | [samirsaci/picking-route](https://github.com/samirsaci/picking-route) |
| PuLP, Pyomo | Slotting and labour MILPs | [Optimization tools](../../repos/README.md#optimization-and-routing) |
| RL4CO | RL baselines for routing-style warehouse problems | [ai4co/rl4co](https://github.com/ai4co/rl4co) |
| WareRover | Simulator for joint order scheduling and multi-robot path finding | [arXiv 2602.13999](https://arxiv.org/abs/2602.13999) (links to the project) |
| Datasets | Public warehouse task data is scarce. Order data such as Olist can stand in for order profiles | [datasets](../../datasets/README.md) |

## Open problems
- **Labour planning when robots take part of the work** (see [open problems](../open-problems.md), #8). Robot capacity varies with charging, faults and congestion, so a fixed robot rate understates the variance labour must cover.
- **Rescheduling docks in real time without creating new conflicts.** There is no agreed measure of how much churn a dock and yard team can absorb.
- **Public benchmarks with real warehouse structure.** Most learned results use synthetic layouts and order streams. No public dataset pairs WMS task history with layout and inventory accuracy.
- **Coupled decisions.** Slotting, batching, routing and robot traffic are optimized separately in most sites and most papers. [WareRover](https://arxiv.org/abs/2602.13999) shows that methods tuned for one sub-problem falter when they are coupled.
- **Results from one operator.** The largest fleet results come from the operator that owns the robots and the data ([DeepFleet](https://arxiv.org/abs/2508.08574)). Independent replication is not possible without shared data.
- **Trustworthy stock records.** AI models inherit inventory errors. Vision-based counting could fix this, but there is no public, independent evaluation of its accuracy.

## Further reading
- John Bartholdi and Steven Hackman, [*Warehouse & Distribution Science*](https://www.warehouse-science.com/book/), free PDF (version 0.98.1, 2019). The standard quantitative text on layout, slotting and order picking.
- René de Koster, Tho Le-Duc and Kees Jan Roodbergen, [Design and control of warehouse order picking](https://doi.org/10.1016/j.ejor.2006.07.009), *European Journal of Operational Research*, 2007.
- MITx [MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM) (MIT Learn, free to audit).
- MIT OpenCourseWare, [ESD.273J Logistics and Supply Chain Management](https://ocw.mit.edu/courses/esd-273j-logistics-and-supply-chain-management-fall-2009/).
- Industry bodies: [MHI](https://www.mhi.org/) (material handling industry association), [GS1](https://www.gs1.org/) (SSCC, GTIN, EPCIS), [ASCM SCOR Digital Standard](https://www.ascm.org/corporate-transformation/standards-tools/scor-ds/), [CSCMP](https://www.cscmp.org/).
