# 02. Source: suppliers and procurement

## Decisions
Which suppliers to use, at what price and terms, and how to manage their risk and performance.

## Data
Contracts, invoices, supplier questionnaires, quality records, delivery performance, external risk signals.

## What fits
| Sub-problem | Type | Reach for |
|---|---|---|
| Reading contracts, invoices, certificates | Documents | Document AI plus validation rules |
| Supplier follow-up | Coordination | LLM agents with approval on commitments |
| Award decisions | Planning | Optimization over cost, risk and capacity |
| Supplier risk | Prediction | Risk scoring on external signals, knowledge graphs of tiers |

## Key papers
Full list: [papers](../../papers/2025-2026.md).
- [When LLM agents negotiate: dynamic bargaining in supply chains](https://arxiv.org/abs/2608.07538)
- [Instructing LLMs to negotiate with verifiable rewards](https://arxiv.org/abs/2604.09855)
- [Counterparty modeling is not strategy](https://arxiv.org/abs/2605.16575)
- [Helicase: supply chain knowledge graphs with multi-agent LLMs](https://arxiv.org/abs/2605.26835)
- [LLM-grounded supply chain risk early warning](https://arxiv.org/abs/2603.04818)
- [Automating disruption monitoring with agents](https://arxiv.org/abs/2601.09680)

## Open problems
- Visibility past tier-1 suppliers is thin and expensive to build.
- Supplier fatigue: small suppliers get a different questionnaire from every customer.
- Measuring the value of a risk signal before the disruption happens.
