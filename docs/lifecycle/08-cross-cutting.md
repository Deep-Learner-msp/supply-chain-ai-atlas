# 08. Cross-cutting: risk, sustainability, data sharing

## Scope 3 emissions
EcoVadis and Kearney's 2026 Carbon Action Report (56,000 companies) found only 4% use primary supplier data for Scope 3. California SB 253 requires Scope 1 and 2 reports from November 10, 2026, and Scope 3 from 2027.

| Sub-problem | Reach for |
|---|---|
| Activity data from paperwork | Document AI |
| Filling supplier gaps | ML estimates with uncertainty bands |
| Supplier follow-up | Agents |
| Exchange | WBCSD PACT product carbon footprint standard |

## Data sharing between companies
Electronic bills of lading were about 11% of adoption by mid-2025 (DCSA); nine major ocean carriers committed to 100% by 2030. The barrier is participation and law, not technology.

## Run it
- [02-scope3-spend-vs-activity](../../implementations/02-scope3-spend-vs-activity)
- [08-scope3-uncertainty](../../implementations/08-scope3-uncertainty)
- [07-federated-forecasting](../../implementations/07-federated-forecasting)

## Key papers
Full list: [papers](../../papers/2025-2026.md).
- [GHGbench](https://arxiv.org/abs/2605.13743)
- [Scope3Trace](https://arxiv.org/abs/2607.17122)
- [Carbon-aware AI in supply chain systems](https://arxiv.org/abs/2609.14881)
- [Graph-based digital twins](https://arxiv.org/abs/2504.03692)
- [Synthetic supply chain data with LLM knowledge graphs](https://arxiv.org/abs/2605.26823)
- [Agentic AI autonomy assessment and governance](https://arxiv.org/abs/2607.25405)

## Open problems
- Will auditors accept model-filled emissions figures?
- Fair value splits for shared models between competitors.
- Allocating one factory's emissions across many customers.
