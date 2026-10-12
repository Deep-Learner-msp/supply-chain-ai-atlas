# 08. Cross-cutting: risk, sustainability, data sharing

Three problems cut across every stage from plan to return. **Risk and resilience**: what happens when a supplier, port or lane goes down, and how long you can keep serving customers. **Scope 3 and sustainability**: the emissions in your suppliers' and carriers' operations, which for most companies are the bulk of the footprint and the part you control least. **Data sharing and visibility**: getting several companies to agree on what happened, without handing over data they will not share.

They are grouped because they share a root cause: the facts sit in other companies' systems. Ownership is usually a central team (risk, sustainability, procurement or a control tower) with no authority over the partners who hold the data. Most of the work is coordination and data quality, and that is where AI is most useful.

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Which suppliers, sites and lanes to single-, dual- or multi-source | Strategic | Procurement, supply chain leadership | Yearly, at sourcing events |
| How much buffer stock and spare capacity to hold against disruption | Tactical | Supply planning, finance | Quarterly |
| Which nodes to map past tier 1, and how deeply | Tactical | Procurement, risk | Quarterly |
| Respond to a live disruption: reallocate, expedite, switch supplier | Operational | Control tower, planners | Hours to days |
| Scope 3 method per category: spend-based, activity-based, supplier-specific | Strategic | Sustainability, finance | Yearly, before each report |
| Which suppliers to ask for primary emissions data first | Tactical | Sustainability, procurement | Quarterly |
| Mode, carrier and route choice with an emissions constraint | Operational | Transport | Per shipment or tender |
| Decarbonisation targets and supplier engagement programmes | Strategic | Leadership, sustainability | Yearly |
| Which partners and standards to share data with (EDI, APIs, EPCIS, eBL, data spaces) | Strategic | IT, logistics, legal | Per partnership |
| What each partner may see and how value is split from shared models | Strategic | Legal, commercial | Per partnership |

## KPIs
| Metric | Definition or formula | Why it matters |
|---|---|---|
| Time to recover (TTR) | Time for a node (supplier site, warehouse, port) to be back at full function after a disruption ([Simchi-Levi, Schmidt and Wei, HBR 2014](https://hbr.org/2014/01/from-superstorms-to-factory-fires-managing-unpredictable-supply-chain-disruptions); [MIT News](https://news.mit.edu/2022/companies-use-mit-research-identify-respond-supply-chain-risks-0615)) | Usually estimated by the supplier; the input most often guessed |
| Time to survive (TTS) | Maximum time the chain can still match supply with demand after the node goes down, using inventory, pipeline stock and alternative sources (same sources) | You can compute this yourself. If TTS < TTR, you have exposure |
| Performance impact and Risk Exposure Index | Performance impact (PI): lost units, sales or profit if a node is down for its TTR, with the best response solved as a linear program. REI = PI of the node / maximum PI over all scenarios, so the worst node scores 1 ([Simchi-Levi et al. 2015, *Interfaces*](https://dspace.mit.edu/entities/publication/d44ef29a-78b6-4ec5-a537-d6e4c4f3f55a) (open copy; doi:10.1287/inte.2015.0804)) | Ranks nodes by impact, not by guessed probability. At Ford, the largest risks came from small suppliers of cheap parts, not strategic suppliers ([MIT News](https://news.mit.edu/2022/companies-use-mit-research-identify-respond-supply-chain-risks-0615)) |
| Single-source share | Share of spend, or of parts, with only one qualified supplier | A simple structural exposure measure |
| Tier-n visibility | Share of spend (or of critical parts) whose tier-2 and deeper sites are known | You cannot compute TTS for a node you cannot see |
| Scope 3 primary-data share | Share of Scope 3 emissions calculated from supplier-specific or activity data, rather than spend-based averages | Tracks how much of the number reflects real operations. EcoVadis found 4% of rated companies report primary Scope 3 data |
| Emissions intensity per tonne-km | Transport GHG emissions (well-to-wheel, CO2e) / transport activity (tonne-km), the intensity metric in ISO 14083 and the [GLEC Framework](https://www.smartfreightcentre.org/en/our-programs/emissions-accounting/global-logistics-emissions-council/calculate-report-glec-framework/) | Compares carriers, modes and lanes on one basis |
| Scope 3 uncertainty range | Width of the 90% interval on total Scope 3, from Monte Carlo over factor and data uncertainty | One number hides how much is guessed; see [demo 08](../../implementations/08-scope3-uncertainty) |
| Supplier engagement rate | Share of in-scope suppliers (by spend or emissions) with targets or shared footprints | Scope 3 cuts happen at suppliers; target-setting bodies such as [SBTi](https://sciencebasedtargets.org/net-zero) look at supplier engagement |
| Partner connectivity | Share of shipments, orders or partners exchanged electronically (EDI, API, eBL), not by email or PDF | The base for every visibility and agent use case |
| Event latency and completeness | Time from a physical event (departed, arrived) to the record; share of expected events received | Late or missing events make every downstream model wrong |

## Data and systems
| Area | Data | Systems and standards |
|---|---|---|
| Risk | Supplier and site lists, bills of materials, part-to-site mapping, inventory and pipeline, lead times, news and weather feeds, sanctions lists | ERP, supplier management, risk monitoring services, control towers |
| Scope 3 | Spend by supplier and category, shipment weights and distances, fuel bills, supplier product carbon footprints, emission factor databases | ERP, transport management, [GHG Protocol Scope 3 Standard](https://ghgprotocol.org/corporate-value-chain-scope-3-standard) (categories 1 purchased goods, 4 upstream and 9 downstream transport), ISO 14083 and GLEC for transport, [PACT Methodology v3](https://www.wbcsd.org/resources/pact-methodology-version-3/) (released 30 April 2025) for product footprints |
| Data sharing | Orders, shipment events, bills of lading, product identifiers, certificates | EDI (X12, EDIFACT), [GS1 EPCIS](https://www.gs1.org/standards/epcis), [DCSA](https://dcsa.org/) standards for ocean shipping, data spaces such as [Catena-X](https://catena-x.net/), the [PACT Network](https://www.carbon-transparency.org/) for carbon data |

## Classical methods that work
| Problem | Classical method | Reference |
|---|---|---|
| Ranking disruption risk | TTR and TTS per node, solved as a linear program over the supply network; rank by impact | Simchi-Levi, Schmidt and Wei (2014), [HBR](https://hbr.org/2014/01/from-superstorms-to-factory-fires-managing-unpredictable-supply-chain-disruptions); Simchi-Levi et al. (2015), [Simchi-Levi et al. 2015, *Interfaces*](https://dspace.mit.edu/entities/publication/d44ef29a-78b6-4ec5-a537-d6e4c4f3f55a) (open copy; doi:10.1287/inte.2015.0804) |
| Choosing a mitigation | Compare mitigation (inventory, dual sourcing, held in advance) with contingency (rerouting, backup capacity, used after) | Tomlin (2006), "On the value of mitigation and contingency strategies for managing supply chain disruption risks", *Management Science*, doi:10.1287/mnsc.1060.0515 |
| Disruption models in general | Inventory, sourcing and network design models with disruptions | Snyder et al. (2016), "OR/MS models for supply chain disruptions: a review", *IIE Transactions*, doi:10.1080/0740817X.2015.1067735 |
| Dual sourcing | Split orders between a cheap slow supplier and a fast expensive one | See [10-dual-sourcing](../../implementations/10-dual-sourcing) |
| Scope 3, first pass | Spend-based: spend by category × environmentally extended input-output (EEIO) factor | [USEPA supply chain emission factors](https://github.com/USEPA/supply-chain-factors), [EXIOBASE 3](https://zenodo.org/records/5589597) |
| Scope 3, transport | Activity-based: tonne-km × mode intensity, per ISO 14083 and GLEC | [GLEC Framework](https://www.smartfreightcentre.org/en/our-programs/emissions-accounting/global-logistics-emissions-council/calculate-report-glec-framework/) |
| Scope 3, purchased goods | Supplier-specific product carbon footprints, exchanged in a standard format | [PACT Methodology v3](https://www.wbcsd.org/resources/pact-methodology-version-3/) |
| Uncertainty | Monte Carlo over emission factors and data quality | [demo 08](../../implementations/08-scope3-uncertainty) |
| Data sharing | Agreed message standards and identifiers first; neutral platforms second | EDI, GS1, DCSA |

## What fits
Types follow the [fit guide](../technology/fit-guide.md).

### Risk and resilience
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Spotting disruptions in news, weather and filings | Documents + coordination | LLM extraction into a fixed event schema, matched to your supplier sites, with sources attached | Alerts with no link to which of your parts are affected |
| Mapping tier-2 and deeper suppliers | Shared truth + documents | Knowledge graphs built from filings, customs data and supplier surveys, with confidence on each link | Treating a model-inferred link as confirmed |
| Exposure ranking (TTR, TTS) | Planning | Linear programming over the network, as in the classical method | Likelihood-times-impact scores with guessed probabilities |
| Predicting supplier delay or failure | Prediction | Gradient-boosted trees or graph models on delivery history and financial signals | Black-box scores with no evidence a planner can check |
| Choosing a mitigation | Planning | Stochastic optimization or simulation of inventory and sourcing options | An LLM picking the mitigation |
| Running the response (emails, rebooking, allocation) | Coordination | Agents with allowed actions and human approval | Fully autonomous switching of suppliers |

### Scope 3 emissions
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Activity data from paperwork | Documents | Document AI on invoices, bills of lading and fuel receipts, with validation rules | Unchecked LLM reads |
| Matching spend lines or parts to emission factors | Prediction + documents | LLM or embedding matching with a human check on low-confidence matches | Silent auto-matching with no review queue |
| Filling supplier gaps | Prediction | ML estimates with uncertainty bands | A single point estimate presented as fact |
| Deciding which suppliers to engage | Planning | Rank by contribution to uncertainty, not by size ([demo 08](../../implementations/08-scope3-uncertainty)) | Emailing the biggest suppliers first by default |
| Supplier follow-up | Coordination | Agents | Agents that accept any number a supplier sends |
| Exchange | Shared truth | WBCSD PACT product carbon footprint standard | Bespoke spreadsheets per customer |
| Low-carbon mode and route choice | Planning | Solvers with an emissions term or cap | Optimizing cost, then reporting emissions afterwards |

### Data sharing and visibility
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Agreeing on what happened | Shared truth | Shared event standards (EPCIS, DCSA) and neutral platforms | Starting with a ledger instead of with who has agreed to join |
| Joint forecasting without sharing raw data | Prediction + shared truth | Federated learning with a local layer per partner | A single shared model that averages away the partner seeing the shock |
| Data partners will not share | Shared truth | Synthetic data, aggregates, clean rooms | Assuming contracts alone will make data flow |
| Turning partner PDFs into events | Documents | Document AI plus validation | Rekeying by hand |

## AI in practice, 2025 to 2026
| What | Verdict | Evidence |
|---|---|---|
| LLM agents watching for disruptions | Promising; evaluated mostly on synthetic scenarios | [Agentic disruption monitoring (2026)](https://arxiv.org/abs/2601.09680): seven agents, F1 0.962 to 0.991 and 3.83 minutes per analysis, across 30 synthesised scenarios plus one case study |
| LLM news summarisation for supplier risk | Working as a reading aid | [LLM news summarisation for risk (2025)](https://arxiv.org/abs/2502.17136); [real-time RAG for supply chain vulnerabilities (2025)](https://arxiv.org/abs/2509.10469) |
| Graph models for resilience and early warning | Research stage; synthetic or narrow benchmarks | [Hypergraph resilience inference (2025)](https://arxiv.org/abs/2511.06208) beats GNN baselines on synthetic benchmarks; [temporal graph attention with LLM explanations (2026)](https://arxiv.org/abs/2603.04818) |
| Agent-built supply chain maps | Useful as a draft that people confirm | [Helicase (2026)](https://arxiv.org/abs/2605.26835) |
| Extracting Scope 3 figures from reports | Working, when every number is tied to a page | [Scope3Trace (2026)](https://arxiv.org/abs/2607.17122); [GHGbench (2026)](https://arxiv.org/abs/2605.13743) gives a shared benchmark with 32,000+ company-year records |
| Emission factor matching with LLMs | Working with review | [Parakeet](https://www.climatechange.ai/papers/neurips2024/52) (*background*, NeurIPS 2024): 88.4% precision at 1, so about one match in nine still needs a person; [BOM-to-LCA entity linking (2025)](https://arxiv.org/abs/2502.07418) |
| Primary data in Scope 3 | The real bottleneck, not modelling | EcoVadis and Kearney's [2026 Carbon Action Report](https://ecovadis.com/insights/carbon-report/) (56,000 companies rated): only 4% report primary Scope 3 data, and companies relying on low-reliability data may underestimate Scope 3 by 2.7 times |
| Electronic bills of lading | Slow; participation and law, not technology | About 11% of bills of lading were electronic by August 2025, up from just over 1% in 2021 ([DCSA, via Breakbulk](https://breakbulk.news/shipping-industry-pushes-toward-electronic-bills-of-lading-as-adoption-reaches-11-in-2025/)). Nine major carriers have committed to 100% by 2030 ([DCSA](https://dcsa.org/standards/booking/adoption-guide-booking-and-bill-of-lading)) |
| Federated learning between partners | Ready for pilots; incentives are the hard part | [demo 07](../../implementations/07-federated-forecasting); see the [fit guide](../technology/fit-guide.md) |
| "AI predicts every disruption" | Hype | Major disruptions are rare and different each time. The proven gain is faster detection and impact mapping, not prediction |

### Regulation that sets the pace
| Rule | What it requires | Source |
|---|---|---|
| California SB 253 | Large companies doing business in California report Scope 1 and 2 by November 10, 2026 (delayed from August 10), and Scope 3 from 2027 | [Sidley, June 2026](https://environmentalhealthsafetybrief.sidley.com/2026/06/30/sb-253-update-carb-delays-reporting-deadline-to-november-2026-and-proposes-to-clarify-requirements/) |
| CountEmissionsEU | A common EU method for transport emissions based on EN ISO 14083:2023. Publishing is voluntary, but published figures must use the method. Political agreement announced 6 November 2025 | [European Commission](https://transport.ec.europa.eu/news-events/news/commission-welcomes-political-agreement-new-rules-harmonise-transport-emissions-calculations-eu-2025-11-06_en) |
| EU eFTI, Regulation (EU) 2020/1056 | Authorities must accept electronic freight transport information from July 2027 | [Regulation](https://eur-lex.europa.eu/eli/reg/2020/1056/oj); [Traficom](https://traficom.fi/en/transport-system/connected-and-automated-transport/about-electronic-freight-transport-information-efti) |
| EU Battery Regulation (EU) 2023/1542 | From 18 February 2027, EV, light-transport and industrial batteries over 2 kWh need a digital battery passport (Article 77) | [Regulation](https://eur-lex.europa.eu/eli/reg/2023/1542/oj) |

## Worked example: time to survive vs time to recover
*Illustrative numbers.* A plant uses 1,000 units a day of a cheap bracket from one supplier site. The site floods. The supplier says it will take 42 days to recover (TTR). The plant has 6,000 units on hand and 3,000 in transit, and a second supplier can deliver 400 a day from day 10.

| Option | Time to survive (days) | Units short over the 42 days | Lost contribution at 50 per unit |
|---|---|---|---|
| As is | 9 | 1,000 (day 9) + 32 × 600 = 20,200 | 1,010,000 |
| Hold 10 more days of stock (+10,000 units) | 25 | 17 × 600 = 10,200 | 510,000 |
| Qualify the second supplier for 800 a day | 9 | 1,000 + 32 × 200 = 7,400 | 370,000 |
| Both: 800 a day and 5 more days of stock | 30 | 12 × 200 = 2,400 | 120,000 |

How to read it:
- TTS (9 days) is far below TTR (42 days), so this cheap part is a major exposure. This is the pattern Simchi-Levi's team found at Ford: low-spend parts with high impact.
- TTS is computed from your own data. TTR comes from the supplier and is the least reliable input, so test what happens if it is 20% longer.
- Extra stock raises TTS but still leaves a gap. A qualified second source cuts the loss most per unit of stock held. The [10-dual-sourcing](../../implementations/10-dual-sourcing) demo explores that trade.
- Where AI helps: finding out within hours that the site flooded, and which of your parts it makes. The calculation itself is a small linear program, not an LLM task.

## Common mistakes
- Ranking risk by likelihood times impact when the likelihood is a guess. Rank by impact (TTR vs TTS) instead.
- Mapping only strategic, high-spend suppliers. The bracket in the example would be missed.
- Buying a news-alert feed with no link from events to your own parts and sites.
- Reporting one Scope 3 number with no uncertainty, then celebrating a "reduction" that is really a price change ([demo 02](../../implementations/02-scope3-spend-vs-activity)).
- Chasing primary data from the largest suppliers first, instead of those causing the most uncertainty.
- Accepting model-filled emissions figures without keeping the evidence trail an auditor will ask for.
- Starting a data-sharing project with the technology (a ledger, a platform) before partners agree to join and on identifiers.
- Treating a federated model as finished: the partner that looks different is often the one seeing the shock first.

## Run it
- [02-scope3-spend-vs-activity](../../implementations/02-scope3-spend-vs-activity): why spend-based Scope 3 can move the wrong way.
- [08-scope3-uncertainty](../../implementations/08-scope3-uncertainty): an honest range, and which supplier to chase first.
- [07-federated-forecasting](../../implementations/07-federated-forecasting): shared models without shared data, and where they break.
- [10-dual-sourcing](../../implementations/10-dual-sourcing): the cost and resilience of a second supplier.

## Key papers
Full list: [papers](../../papers/2025-2026.md).

| Paper | Why read it |
|---|---|
| [GHGbench](https://arxiv.org/abs/2605.13743) | A shared benchmark for company and building emission estimation |
| [Scope3Trace](https://arxiv.org/abs/2607.17122) | Extracting Scope 3 numbers with evidence attached |
| [Carbon-aware AI in supply chain systems](https://arxiv.org/abs/2609.14881) | The carbon cost of the AI itself |
| [Entity Linking using LLMs for Automated Product Carbon Footprint Estimation (2025)](https://arxiv.org/abs/2502.07418) | Mapping bill-of-materials parts to life cycle database entries |
| [Graph-based digital twins](https://arxiv.org/abs/2504.03692) | What a supply chain twin should contain |
| [Synthetic supply chain data with LLM knowledge graphs](https://arxiv.org/abs/2605.26823) | Synthetic data when real data cannot be shared |
| [Agentic AI autonomy assessment and governance](https://arxiv.org/abs/2607.25405) | How much autonomy to grant, and how to govern it |
| [Automating supply chain disruption monitoring via an agentic AI approach](https://arxiv.org/abs/2601.09680) | Agents from news to multi-tier exposure to mitigation |
| [Resilience Inference for Supply Chains with Hypergraph Neural Network (2025)](https://arxiv.org/abs/2511.06208) | Predicting resilience from network structure and inventory paths |
| [LLM-grounded explainable risk early warning](https://arxiv.org/abs/2603.04818) | Risk prediction with explanations checked against evidence |
| [Helicase](https://arxiv.org/abs/2605.26835) | Building supply chain knowledge graphs with agents |
| [Evaluating LLMs in Automated News Article Summarization (2025)](https://arxiv.org/abs/2502.17136) | LLM news summaries for supplier risk monitoring |
| [Real-Time RAG for the Identification of Supply Chain Vulnerabilities (2025)](https://arxiv.org/abs/2509.10469) | Keeping an LLM current on disruptions with retrieval |
| [Federated ensemble forecasting under volatility](https://arxiv.org/abs/2608.21399) | Why averaging dilutes rare regimes, and a fix |

## Tools and datasets
| Resource | Use |
|---|---|
| [Graphs and sustainability tools](../../repos/README.md#graphs-and-sustainability) (SupplyGraph, supply-chain-sustainability) | Graph planning data; CO2 reporting for distribution networks |
| [USEPA/useeior](https://github.com/USEPA/useeior) and [supply-chain-factors](https://github.com/USEPA/supply-chain-factors) | US input-output models and the spend-based emission factors built from them |
| [EXIOBASE 3](https://zenodo.org/records/5589597) | Multi-regional input-output database for spend-based Scope 3 outside the US |
| [openLCA](https://github.com/GreenDelta/olca-app), [Brightway](https://github.com/brightway-lca/brightway2) | Open-source life cycle assessment for product footprints |
| [PACT data exchange protocol](https://github.com/wbcsd/data-exchange-protocol) | Technical specification for exchanging product carbon footprints |
| [OpenEPCIS](https://github.com/openepcis/epcis-repository-ce), [DCSA on GitHub](https://github.com/dcsaorg), [Eclipse Tractus-X](https://github.com/eclipse-tractusx) | Open implementations of event sharing, ocean shipping standards and the Catena-X data space |
| [Open Supply Hub](https://opensupplyhub.org/) | Open map of production facilities, for tier-n mapping |
| [GDELT](https://www.gdeltproject.org/) | Open global news event data for disruption monitoring |
| [NY Fed Global Supply Chain Pressure Index](https://www.newyorkfed.org/research/policy/gscpi) | Macro signal of supply chain stress |
| [Corporate emission reports](../../datasets/README.md) | Extracting Scope 1, 2 and 3 from sustainability reports |

## Open problems
- Will auditors accept model-filled emissions figures?
- Fair value splits for shared models between competitors.
- Allocating one factory's emissions across many customers.
- Trustworthy TTR: suppliers estimate their own recovery time and may be optimistic, which is why the Ford work added TTS ([Simchi-Levi et al. 2015](https://dspace.mit.edu/entities/publication/d44ef29a-78b6-4ec5-a537-d6e4c4f3f55a)). Methods to validate or learn TTR from past events are thin.
- Evaluating disruption models when real disruptions are rare and each is different. Most 2025 to 2026 results use synthetic scenarios.
- Verified primary data at scale: PACT standardises the exchange, but checking that a supplier's footprint is right still needs a person.
- Tier-n maps that suppliers consent to: inferred links are useful, but publishing them can expose a supplier's customers.
- The footprint of the AI used to compute the footprint ([2609.14881](https://arxiv.org/abs/2609.14881)).

## Further reading
- Yossi Sheffi, *The Resilient Enterprise* (MIT Press, 2005). The standard book on disruption and resilience.
- Simchi-Levi, Schmidt and Wei, [From Superstorms to Factory Fires](https://hbr.org/2014/01/from-superstorms-to-factory-fires-managing-unpredictable-supply-chain-disruptions) (HBR, 2014).
- [GHG Protocol](https://ghgprotocol.org/): the [Corporate Standard](https://ghgprotocol.org/corporate-standard), [Scope 3 Standard](https://ghgprotocol.org/corporate-value-chain-scope-3-standard) and [Scope 3 Calculation Guidance](https://ghgprotocol.org/scope-3-calculation-guidance-2).
- ISO 14083:2023, quantification of GHG emissions from transport chain operations, and its practical companion, the [GLEC Framework](https://www.smartfreightcentre.org/en/our-programs/emissions-accounting/global-logistics-emissions-council/calculate-report-glec-framework/) from [Smart Freight Centre](https://www.smartfreightcentre.org/en/).
- [PACT Methodology v3](https://www.wbcsd.org/resources/pact-methodology-version-3/) (WBCSD) and the [PACT site](https://www.carbon-transparency.org/).
- [SBTi Net-Zero](https://sciencebasedtargets.org/net-zero) for target setting.
- [DCSA](https://dcsa.org/) and [GS1 EPCIS](https://ref.gs1.org/standards/epcis/) for data-sharing standards.
- [MIT MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM) and [MIT OCW ESD.273J Logistics and Supply Chain Management](https://ocw.mit.edu/courses/esd-273j-logistics-and-supply-chain-management-fall-2009/), free.
