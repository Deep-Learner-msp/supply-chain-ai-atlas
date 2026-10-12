# Start here

A learning path for people who know AI but not supply chain, or the other way round. For a fuller, ordered curriculum by reader type, see the [learning path](learning-path.md).

## Week 1: the shape of the system
1. Read the [lifecycle overview](../README.md#the-supply-chain-end-to-end) and the eight lifecycle pages, in order.
2. Run [implementation 01](../implementations/01-bullwhip-simulator) and change the lead time. You now understand why supply chains overreact.
3. Learn twenty words from the [glossary](glossary.md): OTIF, dwell, detention, lead time, safety stock, S&OP, 3PL, LTL, BOL, POD, and the rest.
4. Skim the [KPI dictionary](reference/kpis.md) for the stage you care about. Every metric there has a formula and the ways it gets gamed.

## Week 2: the technology fit
1. Read the [fit guide](technology/fit-guide.md). Most failed projects pick the tool before naming the type of problem. Work through its decision checklist on a problem you know.
2. Read one survey from [papers](../papers/2025-2026.md): the LLMs and operations research survey is a good first one.
3. Run [implementation 02](../implementations/02-scope3-spend-vs-activity) and [implementation 09](../implementations/09-safety-stock).
4. Read the [data standards](reference/data-standards.md) map. Agents and document models act through these messages.

## Week 3 onward: go deep on one stage
Pick one lifecycle page. Read its papers, install one of its tools from [repos](../repos/README.md), and try one of its [datasets](../datasets/README.md). Then read its open problems and pick one from the [full list](open-problems.md).

## Building something real
| You want to | Read |
|---|---|
| Build an agent that holds up in production | [Agent architecture](playbooks/agent-architecture.md), then [demo 06](../implementations/06-agent-with-guardrails) and [SCX-Bench](../benchmark) |
| Know whether a model, solver or agent is good enough | [Evaluation](playbooks/evaluation.md) |
| Get from pilot to production | [Deploying AI](playbooks/deploying-ai.md) |

## Reference
| Page | What is in it |
|---|---|
| [Glossary](glossary.md) | Supply chain terms in one line each |
| [KPI dictionary](reference/kpis.md) | Metrics by stage, with formulas and pitfalls |
| [Data standards](reference/data-standards.md) | EDI, GS1, DCSA, PACT and the rest: who owns them and what they carry |
| [Learning path](learning-path.md) | Ordered tracks for engineers, practitioners and researchers, with free outside resources |
| [Open problems](open-problems.md) | Unsolved problems worth a thesis or a startup |

## Formal courses worth the time
- MITx MicroMasters in Supply Chain Management, now on [MIT Learn](https://learn.mit.edu/programs/program-v1:MITxT+SCM): the most rigorous structured option. Free to audit; the certificate track is paid.
- *Forecasting: Principles and Practice* by Hyndman and Athanasopoulos: free online at [otexts.com/fpp3](https://otexts.com/fpp3/).
- *Warehouse & Distribution Science* by Bartholdi and Hackman: a free textbook at [warehouse-science.com](https://www.warehouse-science.com/).
