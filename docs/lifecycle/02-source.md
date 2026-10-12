# 02. Source: suppliers and procurement

Sourcing decides which suppliers to use, at what price and terms, how much to buy from each, and how to manage their risk and performance over time. It is owned by procurement: category managers and strategic buyers for the big decisions, buyers and supplier quality engineers for day-to-day work, with risk, legal and finance involved in contracts and compliance. It matters because purchased goods and services are usually the largest cost line for a manufacturer or retailer, supplier lead-time reliability drives safety stock in [Plan](01-plan.md), and most disruptions start upstream. Visibility thins quickly past direct suppliers: in McKinsey's 2024 survey of 88 supply chain leaders, 60% reported comprehensive visibility of tier-one suppliers, while the share with good visibility into deeper tiers fell by seven percentage points for the second year running ([McKinsey, 2024](https://karriere.mckinsey.de/capabilities/operations/our-insights/supply-chain-risk-survey-2024)).

The short version: reading contracts and invoices is a Documents problem, award and allocation is a Planning problem, supplier risk is a Prediction problem over a graph you only partly know, and chasing suppliers is a Coordination problem. Negotiation sits between Coordination and Planning, and needs the strictest guardrails.

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Category strategy (segment spend, e.g. with a Kraljic matrix) | Strategic | Category manager, CPO | Yearly |
| Make or buy, supplier base size, single versus dual sourcing | Strategic | CPO with operations and finance | Yearly, or after a disruption |
| Supplier selection and qualification | Strategic | Category manager, supplier quality | Per sourcing event |
| Contract terms: price, indexation, payment terms, penalties, capacity reservations | Tactical | Category manager, legal | Per contract, often 1 to 3 years |
| Award and volume allocation across suppliers | Tactical | Category manager | Per tender, or quarterly |
| Supplier risk monitoring and mitigation plans | Tactical | Risk or supplier management team | Continuous, reviewed monthly |
| Supplier performance reviews and corrective actions | Tactical | Supplier quality, buyer | Quarterly |
| Purchase orders, releases, expediting | Operational | Buyer, MRP | Daily |
| Invoice matching and dispute resolution | Operational | Accounts payable, buyer | Daily |
| Tail-spend buying and spot quotes | Operational | Buyer, catalogue or marketplace | Daily |

## KPIs
| Metric | Definition or formula | What good looks like, and why it matters |
|---|---|---|
| Supplier OTIF | Order lines delivered on time and in full divided by order lines due | High and stable. It is the input-side mirror of your customer service level |
| Supplier lead time and its variability | Mean and standard deviation of PO-to-receipt time, measured from receipts | Short and, more importantly, stable: variability drives safety stock (see the [Plan worked example](01-plan.md#worked-example-safety-stock-under-lead-time-variability)) |
| Quality defect rate (PPM) | Defective parts per million received | Low and falling. Each defect is rework, a line stop or a recall risk |
| Purchase price variance (PPV) | `(actual price − standard price) × quantity` | Read with care: favourable PPV bought with worse lead time or quality is a loss elsewhere |
| Total cost of ownership (TCO) | Price plus freight, duties, inventory carrying, quality and risk costs | The comparison basis for awards. Price alone favours far, cheap, fragile suppliers |
| Spend under management | Spend covered by procurement-negotiated contracts divided by total addressable spend | High. Unmanaged spend is where leakage and risk hide |
| Contract compliance | Spend through contracted suppliers and prices divided by spend in that category | High. The negotiated price only counts if buyers use it |
| Realised savings | Validated price reductions versus a baseline, as booked by finance | Booked, not just reported |
| Days payable outstanding (DPO) | `accounts payable / cost of goods sold × 365` | A working-capital lever; pushing it too far shifts risk onto small suppliers |
| Supplier concentration | Share of a category's spend or critical parts with the largest supplier, or with single-source parts | Known and deliberate. Single source is a choice, not an accident |
| Time to recover (TTR) versus time to survive (TTS) | TTR: how long a supplier node takes to return to full output after a disruption. TTS: how long you can keep meeting demand without it | Find the nodes where TTR is longer than TTS. They need mitigation ([Simchi-Levi, Schmidt and Wei, 2014](https://hbr.org/2014/01/from-superstorms-to-factory-fires-managing-unpredictable-supply-chain-disruptions)) |

## Data and systems
| Data | Typical source | Notes |
|---|---|---|
| Purchase orders, receipts, invoices | ERP, procure-to-pay system, EDI 850 / 855 / 856 / 810 | The ground truth for lead times and OTIF; invoices arrive as EDI, PDF or e-invoices |
| Contracts and amendments | Contract lifecycle management (CLM) system, shared drives | Mostly unstructured; terms that matter (indexation, penalties, termination) are buried in clauses |
| Spend cube | Spend analytics, built from AP and PO data | Needs classification into a taxonomy such as UNSPSC; supplier names need de-duplication |
| Supplier master data | Supplier relationship management (SRM), ERP vendor master | Duplicates, stale contacts and missing parent companies are the norm |
| Quality records | QMS, inspection results, corrective action reports | Ties defects to suppliers and parts |
| Supplier questionnaires and certificates | SRM portals, email | Repetitive; each customer asks the same supplier different questions |
| External risk signals | News, sanctions lists, weather, port and trade data, financial filings | Noisy and unstructured; mapping events to your suppliers is the hard step |
| Sub-tier and facility data | Supplier disclosures, bills of materials, [Open Supply Hub](https://opensupplyhub.org/), [UN Comtrade](https://comtradeplus.un.org/) | Incomplete by nature; treat every sub-tier link as uncertain |

Systems: ERP and procure-to-pay hold transactions. Sourcing and e-auction tools run tenders. CLM holds contracts. SRM holds supplier data, scorecards and risk. Standards worth knowing: [GS1](https://www.gs1.org/standards) identifiers ([GLN](https://www.gs1.org/standards/id-keys/gln) for supplier sites), ANSI X12 and UN/EDIFACT for orders and invoices, [Peppol](https://peppol.org/) and the European e-invoicing standard EN 16931 for structured invoices, and UNSPSC for spend classification.

Regulation increasingly makes sub-tier knowledge mandatory. Examples: the US [Uyghur Forced Labor Prevention Act](https://www.cbp.gov/trade/forced-labor/UFLPA), enforced at the border by CBP, and the EU Corporate Sustainability Due Diligence Directive ([Directive (EU) 2024/1760](https://eur-lex.europa.eu/eli/dir/2024/1760/oj)), whose application dates were pushed back by the "stop-the-clock" [Directive (EU) 2025/794](https://eur-lex.europa.eu/eli/dir/2025/794/oj). Check the current consolidated text before relying on any date or threshold.

## Classical methods that work
| Method | Use it for | Reference |
|---|---|---|
| Kraljic portfolio matrix (profit impact versus supply risk: strategic, leverage, bottleneck, non-critical) | Choosing a strategy per category | [Kraljic, 1983](https://hbr.org/1983/09/purchasing-must-become-supply-management), *background* |
| Weighted scoring and multi-criteria methods (AHP and similar) | Supplier selection with several criteria | [Weber, Current and Benton, 1991](https://doi.org/10.1016/0377-2217%2891%2990033-R), *background* review of criteria and methods |
| Total cost of ownership models | Comparing offers on landed cost, not price | Standard procurement practice |
| Mixed-integer programming for award allocation | Splitting volume across bids with capacity, minimums and risk limits | Solvers in [OR-Tools](https://github.com/google/or-tools), [PuLP](https://github.com/coin-or/pulp), [Pyomo](https://github.com/Pyomo/pyomo) |
| Tailored base-surge dual sourcing | A cheap offshore base rate plus a responsive nearshore surge | [Allon and Van Mieghem, 2010](https://ideas.repec.org/a/inm/ormnsc/v56y2010i1p110-124.html), *background* |
| Dual-index policies | Ordering from a fast and a slow supplier with simple rules | [Veeraraghavan and Scheller-Wolf, 2008](https://ideas.repec.org/a/inm/oropre/v56y2008i4p850-864.html), *background* |
| Mitigation versus contingency analysis | When to hold inventory, dual source, or accept disruption risk | [Tomlin, 2006](https://ideas.repec.org/a/inm/ormnsc/v52y2006i5p639-657.html), *background*: frequent-short versus rare-long disruptions favour different strategies |
| Impact-first risk exposure (TTR/TTS) | Ranking supplier nodes by the damage their failure would do, before estimating probabilities | [Simchi-Levi et al., 2015](https://ideas.repec.org/a/inm/orinte/v45y2015i5p375-390.html), *background*: a three-year engagement with Ford |
| Three-way match (PO, receipt, invoice) with tolerances | Catching invoice errors before payment | Standard accounts payable control |
| Supplier scorecards on OTIF, quality and responsiveness | Performance management | Standard practice; the value is in acting on them |

## What fits
| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Reading contracts, invoices, certificates | Documents | Document AI or vision-language models plus validation rules (three-way match, totals, master data checks) | An LLM read with nothing checking its output |
| Spend classification and supplier de-duplication | Prediction | Text classifiers or LLMs with a fixed taxonomy and human review of low-confidence items | Free-form categories the model invents |
| Supplier follow-up (confirmations, certificates, questionnaires) | Coordination | LLM agents with approval on commitments | Agents that can change prices or terms on their own |
| Tail-spend negotiation | Coordination + Planning | Negotiation agents inside a fixed mandate (price floor, term limits) with automatic profit checks | Unbounded mandates; agent-to-agent deals nobody audits |
| Award and allocation decisions | Planning | Optimization over cost, risk and capacity | Letting an LLM pick the winner |
| Dual sourcing and buffer sizing | Planning | Expected-cost and scenario models, stochastic optimization, simulation | Dual sourcing by rule of thumb |
| Supplier risk | Prediction | Risk scoring on external signals, knowledge graphs of tiers, with evidence attached | A single opaque risk score with no source |
| Sub-tier mapping | Prediction + Documents | Agents that assemble graphs from disclosures and trade data, with per-link confidence | Treating an inferred link as fact |
| Disruption monitoring | Coordination | Agents that read news, map events to your supplier graph and draft actions | Alert floods without exposure analysis |

## AI in practice, 2025 to 2026
| Claim | Verdict | Evidence |
|---|---|---|
| Bots can negotiate long-tail supplier terms | **Working**, for simple terms inside a mandate | Walmart used an automated negotiation tool with suppliers whose agreements were otherwise rarely negotiated ([Van Hoek et al., HBR, 2022](https://hbr.org/2022/11/how-walmart-automated-supplier-negotiations), *background*) |
| LLM agents can negotiate supply contracts autonomously | **Partly**. They agree, but leak value and sometimes sign bad deals | In 9,840 LLM-to-LLM negotiations, agents agreed 98.9% of the time but took 2.98 rounds against 1.25 in equilibrium, eroding 21% to 34% of surplus; baseline models accepted individually irrational contracts in 19.2% of cases ([Liang and Xu, 2026](https://arxiv.org/abs/2608.07538)) |
| LLMs negotiate strategically | **Not yet** | Agents modelled the counterparty's preferences accurately but did not turn that into better deals; outcomes followed opening anchors ([Cosentino et al., 2026](https://arxiv.org/abs/2605.16575)). Training with verifiable rewards helps: a 30B buyer beat much larger frontier models ([Liu et al., 2026](https://arxiv.org/abs/2604.09855)) |
| Agents can monitor disruptions across tiers | **Promising, early** | A seven-agent system reported F1 of 0.962 to 0.991 on 30 synthesised automotive scenarios, at a mean of 3.83 minutes per analysis ([AlMahri, Xu and Brintrup, 2026](https://arxiv.org/abs/2601.09680)). Synthetic scenarios, not live operations |
| LLMs can map sub-tier supply networks | **Promising, early** | Helicase builds query-specific knowledge graphs with per-fact uncertainty and introduces an 80-query benchmark ([Long et al., 2026](https://arxiv.org/abs/2605.26835)) |
| LLM explanations of risk scores can be trusted | **Only when grounded** | Constraining the LLM to model evidence gave 99.6% directional consistency between narrative and evidence, on six months of maritime data ([Xue et al., 2026](https://arxiv.org/abs/2603.04818)) |
| Contract extraction is solved | **No, but useful with review** | Expert-annotated contract review remains hard for models ([CUAD](https://arxiv.org/abs/2103.06268), *background*); fine-tuned models extract industrial contract fields with high recall on their own data ([Cao et al., 2025](https://arxiv.org/abs/2507.06539)) |
| Deep RL for dual sourcing | **Lab stage** | Competitive with heuristics on dual-sourcing benchmarks ([Maggiar et al., 2025](https://arxiv.org/abs/2507.22040)); [Liu, Liu and Eisenach, 2025](https://arxiv.org/abs/2507.14446) report gains on large real-world datasets with supply and capacity risk |
| End-to-end autonomous procurement | **Hype** | No public evidence of agents running strategic sourcing unsupervised. The reliability results above argue for mandates, approvals and automatic profit checks |

## Worked example: when does dual sourcing pay?
*Illustrative numbers.* Annual demand is 100,000 units. Supplier A (offshore) costs $10 per unit and has a 5% chance per year of a 13-week outage. Supplier B (nearshore) costs $11 per unit and has a 2% chance of the same outage. Each unit short costs $30 (lost contribution plus expediting). A full 13-week outage leaves `100,000 × 13/52 = 25,000` units short, so it costs `25,000 × $30 = $750,000`.

Option 3 buys 80% from A and 20% from B, and reserves capacity so B can ramp to 60% of demand if A goes down. A's outage then costs 40% of the full impact. Assume A can absorb B's share if B goes down. The joint outage probability (`0.05 × 0.02 = 0.001`) is ignored.

| Option | Purchase cost | Expected outage cost | Expected total | Loss in an A-outage year |
|---|---|---|---|---|
| 1. Single source A | $1,000,000 | 0.05 × $750,000 = $37,500 | **$1,037,500** | $750,000 |
| 2. Single source B | $1,100,000 | 0.02 × $750,000 = $15,000 | $1,115,000 | n/a |
| 3. 80% A, 20% B, B flexes to 60% | $1,020,000 | 0.05 × $300,000 = $15,000 | **$1,035,000** | $300,000 |

The break-even outage probability for A, where options 1 and 3 cost the same:

```
1,000,000 + 750,000·p = 1,020,000 + 300,000·p   →   p = 20,000 / 450,000 ≈ 4.4%
```

| A's annual outage probability | Single A | Dual (option 3) |
|---|---|---|
| 2% | $1,015,000 | $1,026,000 |
| 5% | $1,037,500 | $1,035,000 |
| 10% | $1,075,000 | $1,050,000 |

What to notice:
- At 5% the two options are almost tied in expectation. Dual sourcing is insurance: its value is mostly in the bad year, where it cuts the loss from $750,000 to $300,000.
- The answer is very sensitive to two numbers procurement rarely has: the outage probability and the cost per unit short. Ranking nodes by impact first ([Simchi-Levi et al., 2015](https://ideas.repec.org/a/inm/orinte/v45y2015i5p375-390.html)) avoids needing a precise probability for every supplier.
- B's flexibility is the real asset. A second supplier that cannot ramp up protects little. Contracts should price the reserved capacity explicitly.

Run the full version, with simulation: [10-dual-sourcing](../../implementations/10-dual-sourcing).

## Common mistakes
- **Awarding on unit price.** Compare total cost of ownership, including lead-time variability and its safety stock cost.
- **Using quoted lead times.** Measure them from receipts; feed the variability into Plan.
- **Dual sourcing without flex.** A second supplier at a fixed 20% share does not cover a 100% outage.
- **Risk scores without evidence.** A number nobody can trace to a source will not change a buyer's decision, and should not.
- **Treating inferred sub-tier links as fact.** Graphs built by models or from trade data need a confidence on every edge.
- **Extraction without validation.** Every field an LLM reads from an invoice or contract should face a rule: three-way match, totals, master data, or a human for low confidence.
- **Giving a negotiation agent an open mandate.** Set price floors, term limits and an automatic check that the deal is better than walking away.
- **Pushing payment terms onto fragile suppliers.** Higher DPO can raise supplier failure risk in exactly the tiers you cannot see.
- **Sending every supplier a new questionnaire.** Reuse standard questionnaires and shared data where they exist.
- **Measuring savings that finance never books.**

## Run it
- [04-llm-solver-interface](../../implementations/04-llm-solver-interface): the LLM translates what-if questions, the solver re-plans; the same pattern applies to award scenarios
- [06-agent-with-guardrails](../../implementations/06-agent-with-guardrails): allowed tools, approvals on money, an audit log; the pattern for supplier follow-up
- [10-dual-sourcing](../../implementations/10-dual-sourcing): dual sourcing and supplier risk

## Key papers
Full list: [papers](../../papers/2025-2026.md).
| Paper | Why read it |
|---|---|
| [When LLM agents negotiate: dynamic bargaining in supply chains](https://arxiv.org/abs/2608.07538) | 9,840 negotiations against a game-theory benchmark: value, division and failure rates |
| [Instructing LLMs to negotiate with verifiable rewards](https://arxiv.org/abs/2604.09855) | Training negotiators on checkable economic rewards |
| [Strategic Bargaining in Multi-Buyer Markets](https://arxiv.org/abs/2607.05863) | Verifiable-reward training when several buyers compete |
| [Counterparty modeling is not strategy](https://arxiv.org/abs/2605.16575) | Why knowing the other side's preferences is not enough |
| [TERMS-Bench](https://arxiv.org/abs/2605.13909) | Scoring negotiation agents beyond "did they agree" |
| [Helicase: supply chain knowledge graphs with multi-agent LLMs](https://arxiv.org/abs/2605.26835) | Sub-tier mapping with per-fact uncertainty |
| [LLM-grounded supply chain risk early warning](https://arxiv.org/abs/2603.04818) | Risk explanations constrained to model evidence |
| [Automating disruption monitoring with agents](https://arxiv.org/abs/2601.09680) | Agents from news to multi-tier exposure to mitigation |
| [Deep RL dual sourcing with supply and capacity risk](https://arxiv.org/abs/2507.14446) | RL for multi-sourcing at scale |
| [Structure-Informed Deep RL for Inventory Management](https://arxiv.org/abs/2507.22040) | Includes dual sourcing; learned policies recover known structure |
| [LLM for extracting complex contract information](https://arxiv.org/abs/2507.06539) | Fine-tuning for industrial contract fields |
| [Enhancing supply chain visibility with KGs and LLMs](https://arxiv.org/abs/2408.07705) | *Background.* The KG-plus-LLM pattern for visibility |

## Tools and datasets
| Resource | Use |
|---|---|
| [OR-Tools](https://github.com/google/or-tools), [PuLP](https://github.com/coin-or/pulp), [Pyomo](https://github.com/Pyomo/pyomo) | Award allocation and sourcing models |
| [stockpyl](https://github.com/LarrySnyder/stockpyl) | Inventory models for buffer sizing alongside sourcing |
| [SupplyGraph](https://github.com/ciol-researchlab/SupplyGraph) | Graph benchmark for supply chain planning |
| [CUAD](https://github.com/TheAtticusProject/cuad) | Expert-annotated contract clauses, for testing extraction |
| [Open Supply Hub](https://opensupplyhub.org/) | Open data on production facilities, for sub-tier mapping |
| [UN Comtrade](https://comtradeplus.un.org/) | Trade flows by product and country, for exposure analysis |

More: [tools](../../repos/README.md), [datasets](../../datasets/README.md).

## Open problems
- Visibility past tier-1 suppliers is thin and expensive to build.
- Supplier fatigue: small suppliers get a different questionnaire from every customer.
- Measuring the value of a risk signal before the disruption happens.
- **Agent-to-agent procurement.** When both buyer and supplier delegate to agents, who audits the deal? Results above show surplus division depends on which model each side uses and how it is prompted.
- **Outage probabilities for rare events.** Dual-sourcing math needs them, history rarely has them, and expert estimates are poorly calibrated.
- **Confidence on inferred supply graphs.** Methods exist to build sub-tier graphs; there is no agreed way to score how right they are, or to combine them with supplier disclosures.
- **Contract terms as data.** Indexation, penalties and capacity reservations live in clauses. Extracting them reliably enough to feed planning and risk models is open.
- **Fairness to small suppliers.** Automation lets large buyers negotiate everyone at once; the effect on supplier margins and resilience is not measured.

See all: [open problems](../open-problems.md).

## Further reading
- Kraljic, [Purchasing must become supply management](https://hbr.org/1983/09/purchasing-must-become-supply-management), HBR, 1983.
- Simchi-Levi, Schmidt and Wei, [From superstorms to factory fires](https://hbr.org/2014/01/from-superstorms-to-factory-fires-managing-unpredictable-supply-chain-disruptions), HBR, 2014.
- Snyder and Shen, [*Fundamentals of Supply Chain Theory*](https://www.wiley.com/en-us/Fundamentals+of+Supply+Chain+Theory%2C+2nd+Edition-p-9781119024842), 2nd edition: supply uncertainty and disruption models.
- MITx [MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM).
- Professional bodies: [CIPS](https://www.cips.org/) and [ISM](https://www.ismworld.org/).
