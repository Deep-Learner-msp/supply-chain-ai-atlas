# 07. Return: reverse logistics

Return covers everything that flows back up the chain: customer returns, warranty and repair units, end-of-lease equipment, unsold stock and reusable packaging. The job is to get each unit to its best next use (resale, refurbishment, parts, recycling) quickly, because most returned goods lose value every week they sit. Ownership is usually split: customer service owns the policy and refund, a returns centre or third-party logistics provider owns receipt and grading, and finance or a recommerce team owns resale. That split is one reason returns are planned last.

The scale is large. US retailers expected 15.8% of 2025 sales, about $849.9 billion, to come back; the online return rate was 19.3%, and retailers estimated 9% of returns were fraudulent ([NRF and Happy Returns, Oct 2025](https://nrf.com/media-center/press-releases/consumers-expected-to-return-nearly-850-billion-in-merchandise-in-2025)). Regulation is also changing the menu: from 19 July 2026, large companies may no longer destroy unsold apparel, clothing accessories and footwear in the EU, and "unsold" includes products returned by consumers. Narrow exceptions remain, such as safety risks, damage beyond repair and failed donation ([ESPR, Regulation (EU) 2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj); [Delegated Regulation (EU) 2026/296](https://eur-lex.europa.eu/eli/reg_del/2026/296/oj); [Linklaters summary](https://sustainablefutures.linklaters.com/post/102miiy/eu-espr-commission-adopts-final-acts-on-unsold-consumer-product-destruction-and)).

## Decisions
| Decision | Horizon | Typical owner | Cadence |
|---|---|---|---|
| Return policy: window, fees, free vs paid, returnless refunds | Strategic | Commercial, customer service, finance | Yearly, seasonal reviews |
| Reverse network: central vs regional returns centres, in-store returns, outsourcing | Strategic | Network design, logistics | Every 2 to 5 years |
| Returns capacity: labour, space and refurbishment slots | Tactical | Returns centre operations | Monthly, peak season |
| Which orders are likely to come back, and what to do before shipping | Operational | E-commerce, merchandising | Per order |
| Accept, refund or flag a return (including fraud checks) | Operational | Customer service, loss prevention | Per return |
| How deeply to inspect a unit before deciding | Operational | Returns centre | Per unit |
| Disposition: restock, refurbish, resell as used, liquidate, harvest parts, recycle or scrap | Operational | Returns centre, recommerce | Per unit or batch |
| Where to send it: which store, warehouse, refurbisher, marketplace or recycler | Operational | Inventory planning | Daily |

## KPIs
There is no single standards body for returns metrics. These are the common working definitions; agree yours in writing before comparing sites or vendors.

| Metric | Definition or formula | Why it matters |
|---|---|---|
| Return rate | Units (or value) returned / units (or value) sold, matched by sales cohort, not calendar month | The demand signal for the whole reverse chain. Calendar-month ratios mix cohorts and lag |
| Return lag | Days from delivery to return receipt, as a distribution | Drives reverse capacity planning and how long a sale is "provisional" |
| Disposition cycle time | Time from receipt at the returns centre to the disposition being executed (back on sale, shipped to refurbisher, recycled) | Value decays with time; this is the clock |
| Refund cycle time | Time from customer handover to refund issued | The customer-facing number; drives repeat purchase |
| Recovery value rate | Net recovery value / original cost (or original net sales value) of the returned units. Net = resale proceeds minus handling, refurbishment and transport | The headline economic measure. State the denominator |
| Refurbish yield | Units that pass final test after refurbishment / units entering refurbishment | Low yield means grading is sending the wrong units to refurbishment |
| Grading accuracy | Share of units whose assigned grade matches an independent audit grade | The input to every disposition rule. Rarely measured, often poor |
| Restock rate | Units resold as new or open-box / units returned | How much returns are really just delayed sales |
| Landfill diversion rate | Weight not sent to landfill or incineration / total returned weight | Sustainability reporting; under ESPR, destruction needs a permitted reason |
| Return fraud rate | Returns found fraudulent / all returns | NRF retailers estimated 9% for 2025; measure your own before buying tools |

## Data and systems
| Data | Where it lives | Notes |
|---|---|---|
| Orders, prices, customer history | Order management system, e-commerce platform | Needed for return propensity and fraud models |
| Return authorisations and reason codes | Returns portal, customer service tool | Reason codes are coarse and often chosen to avoid a fee |
| Free-text return notes and chats | Returns portal, contact centre | Richer than reason codes; needs language models to use at scale |
| Receipt scans, serial numbers | Warehouse management system returns module | Serial numbers link to warranty and fraud checks |
| Inspection results, photos, test logs | Returns centre or refurbisher systems | The ground truth for grading models, if kept |
| Refurbishment work orders, parts used | Repair or refurbishment system | Needed for yield and cost per grade |
| Secondary-market prices | Marketplaces, liquidation auctions, recommerce partners | The value side of every disposition decision |
| Recycling and destruction certificates | Recyclers, waste contractors | Compliance evidence (for example under the EU [WEEE Directive](https://eur-lex.europa.eu/eli/dir/2012/19/oj) for electronics and ESPR for textiles) |

Systems: a returns management system or portal, the warehouse management system, an order management system, and often a third-party logistics provider's systems in between. Returns data is usually split across at least three companies, which is why a unit's history is hard to reconstruct.

## Classical methods that work
These are the baselines any AI method has to beat.

| Problem | Classical method | Reference |
|---|---|---|
| Forecasting return volumes | Distributed lag models: returns as a lagged function of past sales, with a return probability and a lag distribution estimated from history | Kelle and Silver (1989), "Forecasting the returns of reusable containers", *Journal of Operations Management*, doi:10.1016/S0272-6963(89)80003-8; Toktay, Wein and Zenios (2000), "Inventory management of remanufacturable products", *Management Science*, doi:10.1287/mnsc.46.11.1412.12082 |
| Reverse network design | Facility location MILP with return flows and uncertain volumes | [Fleischmann et al. (1997), "Quantitative models for reverse logistics: a review"](https://doi.org/10.1016/S0377-2217%2897%2900230-0), *EJOR* |
| Centralised vs fast regional processing | Match network to the item's rate of value decay: efficient, centralised for slow-decay items; responsive, early grading for fast-decay items | Blackburn, Guide, Souza and Van Wassenhove (2004), "Reverse supply chains for commercial returns", *California Management Review*, doi:10.2307/41166207; Guide et al. (2006), "Time value of commercial product returns", *Management Science*, doi:10.1287/mnsc.1060.0522 |
| Disposition | Expected-value rule per grade: pick the option with the highest net recovery value, using a grading checklist | See the worked example below; [Govindan, Soleimani and Kannan (2015) review](https://doi.org/10.1016/j.ejor.2014.07.012) |
| Inventory with returns | Inventory policies that treat returns as a second, uncertain source of supply | Toktay, Wein and Zenios (2000), above |
| Fraud | Rules: serial-number match, receipt match, return frequency limits | Industry practice |

The field's map: Guide and Van Wassenhove (2009), "The evolution of closed-loop supply chain research", *Operations Research*, doi:10.1287/opre.1080.0628.

## What fits
Types follow the [fit guide](../technology/fit-guide.md).

| Sub-problem | Type | Reach for | Avoid |
|---|---|---|---|
| Return volume forecasting | Prediction | Distributed lag model on sales cohorts; gradient-boosted trees with order features; time-series models for aggregate volume | Forecasting returns from returns history alone, ignoring what was sold |
| Return propensity at order time | Prediction | Gradient-boosted trees or graph models on customer, product and size history | Using the score to refuse service without a human policy decision |
| Size and fit (the upstream fix) | Prediction | Size recommendation and size-flag models | Treating returns as purely a logistics problem |
| Return reason extraction | Documents | LLM on free-text notes into a fixed reason list, with confidence | Trusting customer-chosen reason codes as ground truth |
| Condition grading from photos | Prediction (vision) | Vision models trained on your own audited grades, with a human check on low confidence | A general vision-language model grading with no audit set |
| Inspection depth | Planning | Value-of-information rule: inspect when the expected gain exceeds inspection cost | Inspecting everything, or nothing, by habit |
| Disposition | Prediction + planning | Grade probabilities feeding an expected-value or optimization rule | An LLM choosing the disposition directly |
| Allocation of returned stock to stores or channels | Planning | Optimization or reinforcement learning against an offline optimum | Learned policies with no comparison to the offline solution |
| Reverse network design | Planning | Facility location MILP with scenario volumes | Copying the forward network |
| Return fraud | Prediction | Anomaly and graph models plus rules, with human review | Fully automatic refusals |
| Customer and carrier follow-up | Coordination | Agents with a fixed list of allowed actions; human approval on refunds above a limit | Agents issuing refunds unchecked |
| Unit history across companies | Shared truth | Shared identifiers (serial number, GS1 keys) and event standards such as [GS1 EPCIS](https://www.gs1.org/standards/epcis) | A ledger before partners agree on identifiers |

## AI in practice, 2025 to 2026
| What | Verdict | Evidence |
|---|---|---|
| Predicting returns at order time | Works in published studies; gains come from customer and product history, not model novelty | [Returnformer](https://pmc.ncbi.nlm.nih.gov/articles/PMC12839650/) (2026) uses a graph transformer on user and product links and beats four ML baselines on its data; [Karl's review](https://doi.org/10.1007/s11301-024-00436-x) covers 25 returns forecasting studies |
| Size and fit models | Working; the cheapest return is the one that never happens | [SizeFlags](https://arxiv.org/abs/2106.03532) (*background*, 2021) on size-related returns in fashion |
| Reinforcement learning for returned-stock allocation | Promising, simulated only so far | [Linden et al. (2025)](https://arxiv.org/abs/2501.14394) report a 3% gap to the offline optimum and a 96% cut in average storage time, on simulated data |
| LLMs reading return notes to guide inspection | Useful in narrow cases; not a general win | [Semantic signal-assisted inspection (2026)](https://arxiv.org/abs/2609.02116): on three synthetic scenarios, note-guided inspection added value mainly in the aircraft scenario, and a comparator that skipped inspection entirely still scored higher under a purely economic objective |
| Photo-based condition grading | Sold by many vendors, with no public benchmark to compare them | No 2025 to 2026 peer-reviewed benchmark found; treat accuracy claims as unverified until tested on your audited units |
| Returns agents (customer chat, label, refund) | Ready with limits, like other coordination agents | See [06 agent with guardrails](../../implementations/06-agent-with-guardrails) for the pattern |
| "AI eliminates returns" | Hype | Returns are a policy and product-fit problem first. The 2025 rate was still 15.8% ([NRF](https://nrf.com/media-center/press-releases/consumers-expected-to-return-nearly-850-billion-in-merchandise-in-2025)) |

## Worked example: when is inspection worth it?
*Illustrative numbers.* A returned laptop arrives. A model reading the return note and order history gives grade probabilities: A (like new) 0.60, B (worn) 0.25, C (faulty) 0.15. Net recovery values by option and grade:

| Option | Grade A | Grade B | Grade C | Expected value, no inspection |
|---|---|---|---|---|
| Restock as open-box | 620 | 300 | -50 | 0.60×620 + 0.25×300 + 0.15×(-50) = **439.5** |
| Refurbish | 440 | 440 | 260 | 413.0 |
| Liquidate as-is | 300 | 220 | 120 | 253.0 |
| Recycle | 25 | 25 | 25 | 25.0 |

- **Without inspection**, restock every unit: expected 439.5.
- **With perfect inspection**, pick the best option per grade (A restock 620, B refurbish 440, C refurbish 260): 0.60×620 + 0.25×440 + 0.15×260 = 521.0.
- **Expected value of perfect information** = 521.0 - 439.5 = 81.5 per unit. An inspection costing 18 pays 63.5 per unit, or 635,000 per 10,000 units.
- Now suppose a better model says A 0.90, B 0.05, C 0.05. Blind restock is worth 570.5, perfect inspection 593.0, so inspection is worth only 22.5: barely above its cost of 18. A real inspection is not perfect, so its value is lower still.

The lesson: grading models do not just save inspection labour. They change *which* units are worth inspecting. Route confident units straight to disposition and inspect the uncertain ones. The same logic is what [arXiv 2609.02116](https://arxiv.org/abs/2609.02116) tests at batch scale.

## Common mistakes
- Forecasting returns with calendar ratios instead of sales cohorts and lags, then under-staffing every January.
- Optimizing refund speed and ignoring disposition cycle time, while units lose value on the shelf.
- Treating reason codes as truth. Customers pick the code that avoids a fee.
- Training a grading model on grades nobody audited, then measuring it against the same grades.
- Sending everything to one central returns centre regardless of how fast the item loses value.
- Reporting recovery value without stating the denominator (cost, original price or resale price).
- Letting a return-propensity score quietly block customers, with no policy owner and no appeal.
- Forgetting compliance: under ESPR, destroying returned apparel or footwear in the EU needs a permitted reason and an annual disclosure.

## Run it
- [14-returns-disposition](../../implementations/14-returns-disposition): restock, refurbish, recycle or scrap when the grade is uncertain at first touch.
- [06-agent-with-guardrails](../../implementations/06-agent-with-guardrails): the pattern for a returns or refund agent with approvals.
- [03-forecast-baselines](../../implementations/03-forecast-baselines): baselines to start a return-volume forecast.

## Key papers
Full list: [papers](../../papers/2025-2026.md).
| Paper | Why read it |
|---|---|
| [Reinforcement Learning for Efficient Returns Management (2025)](https://arxiv.org/abs/2501.14394) | Returned-stock allocation as an online multiple knapsack problem; compared against the offline optimum |
| [Semantic Signal-Assisted Inspection and Recovery Allocation in Reverse Logistics (2026)](https://arxiv.org/abs/2609.02116) | Return notes as a signal for inspection depth; honest about where it does not help |
| [Returnformer: A Graph Transformer-Based Model for Predicting Product Returns in E-Commerce (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12839650/) | Return prediction from user and product graphs (*Entropy*, doi:10.3390/e28010072) |
| [Forecasting e-commerce consumer returns: a systematic literature review](https://doi.org/10.1007/s11301-024-00436-x) | *Background* (online 2024). Methods, data and predictors across 25 studies |
| [SizeFlags: Reducing Size and Fit Related Returns in Fashion E-Commerce](https://arxiv.org/abs/2106.03532) | *Background.* Preventing returns upstream |
| [Large Language Models for Supply Chain Decisions (2025)](https://arxiv.org/abs/2507.21502) | Where LLMs speed up supply chain decisions in practice; read before putting an LLM near a disposition rule |
| Guide and Van Wassenhove (2009), "The evolution of closed-loop supply chain research", doi:10.1287/opre.1080.0628 | *Background.* The field's map |

## Tools and datasets
| Resource | Use |
|---|---|
| [Optimization and routing tools](../../repos/README.md#optimization-and-routing) (OR-Tools, PuLP, Pyomo) | Reverse network design and disposition optimization |
| [Forecasting tools](../../repos/README.md#forecasting) (statsforecast, Chronos) | Return-volume forecasting baselines |
| [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) | Real transactions where invoices starting with "C" are cancellations; a small public proxy for returns |
| [Olist Brazilian E-Commerce](../../datasets/README.md) | Orders, delivery times and reviews; useful for return-risk features |
| [GS1 EPCIS](https://www.gs1.org/standards/epcis) and [OpenEPCIS](https://github.com/openepcis/epcis-repository-ce) | Event standard and open repository for tracking a unit's history across companies |

Gap: there is no widely used public dataset of returned units with audited grades, photos and disposition outcomes. See open problems.

## Open problems
- Returns are rarely forecast at all, so reverse capacity is planned last.
- Grading condition from photos consistently enough to automate.
- A public benchmark of returned units with images, audited grades and realised resale value, so grading and disposition methods can be compared.
- Valuing inspection: deciding per unit whether to inspect, given an imperfect grade model and shared labour. Early work exists ([2609.02116](https://arxiv.org/abs/2609.02116)), on synthetic data only.
- Fraud detection that does not punish honest customers: scoring who to review without a hidden blacklist.
- Joining forward and reverse planning: returned units as supply in the next replenishment run, with uncertain timing and grade.
- Proving compliance with destruction bans: an auditable record of why each unit was destroyed, across several companies.

## Further reading
- Rogers and Tibben-Lembke, *Going Backwards: Reverse Logistics Trends and Practices* (Reverse Logistics Executive Council, 1998). The early practitioner survey. [RLEC](https://www.rlec.org/).
- Ferguson and Souza (eds.), *Closed-Loop Supply Chains: New Developments to Improve the Sustainability of Business Practices* (CRC Press, 2010).
- [Govindan, Soleimani and Kannan (2015)](https://doi.org/10.1016/j.ejor.2014.07.012), a long review of reverse logistics and closed-loop research.
- [MIT MicroMasters in Supply Chain Management](https://learn.mit.edu/programs/program-v1:MITxT+SCM) (free to audit) for the forecasting and network design foundations.
- EU [ESPR](https://eur-lex.europa.eu/eli/reg/2024/1781/oj) and [WEEE Directive](https://eur-lex.europa.eu/eli/dir/2012/19/oj), the rules that limit what you may do with returns in the EU.
