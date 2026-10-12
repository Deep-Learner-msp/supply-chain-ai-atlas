# Data standards: the interoperability map

Supply chains are many companies passing messages. Standards decide whether those messages mean the same thing at both ends. This page lists the ones that matter, who owns them and what they carry.

## Why standards matter for AI

| Reason | What it means in practice |
|---|---|
| Agents act through messages | An agent that tenders a load, confirms an appointment or disputes an invoice is sending an EDI 204, a 990 or a 210 under the hood. If it cannot read and write the standard, it cannot act. |
| Shared identifiers make joins possible | GTIN, SSCC and GLN let a forecast, a shipment and a warehouse record point at the same thing. Without them, entity matching eats most of the project. |
| Events are training data | EDI 214, EPCIS and DCSA track and trace events are the labels for ETA, dwell and exception models. Their codes and timestamps set the ceiling on model quality. |
| Standards bound what a model may output | A document AI model that maps a PDF to the fields of an e-CMR or an eBL has a schema to validate against. Free text has none. |
| Emissions numbers must be comparable | A footprint calculated under ISO 14083 or the GLEC Framework can be checked and aggregated. A model-filled number with no method cannot. |
| Data sharing needs a common shape | Federated learning and data spaces still need partners to agree on fields and units first ([demo 07](../../implementations/07-federated-forecasting)). |

## Summary table

| Standard | Owner | What it carries | Where it shows up in this repo |
|---|---|---|---|
| [ANSI X12 EDI](https://x12.org/products/transaction-sets) | X12 (ANSI-accredited) | Orders, ship notices, load tenders, shipment status, invoices (North America) | [04-move](../lifecycle/04-move.md), [glossary](../glossary.md), [demo 06](../../implementations/06-agent-with-guardrails) |
| [UN/EDIFACT](https://unece.org/trade/uncefact/introducing-unedifact) | UN/CEFACT (UNECE) | The same business messages, used internationally and in ocean and customs | [04-move](../lifecycle/04-move.md) |
| [GTIN](https://www.gs1.org/standards/id-keys/gtin) | GS1 | Product identity | [01-plan](../lifecycle/01-plan.md), [05-store](../lifecycle/05-store.md) |
| [SSCC](https://www.gs1.org/standards/id-keys/sscc) | GS1 | Identity of a logistic unit (pallet, case, parcel) | [05-store](../lifecycle/05-store.md), [06-deliver](../lifecycle/06-deliver.md) |
| [GLN](https://www.gs1.org/standards/id-keys/gln) | GS1 | Identity of a party or location (dock, store, plant) | [05-store](../lifecycle/05-store.md), [demo 05](../../implementations/05-dock-scheduling) |
| [GS1 Digital Link](https://www.gs1.org/standards/gs1-digital-link) | GS1 | GS1 identifiers expressed as web URIs, for QR codes and links to product data | [07-return](../lifecycle/07-return.md), [08-cross-cutting](../lifecycle/08-cross-cutting.md) |
| [EPCIS 2.0](https://ref.gs1.org/standards/epcis/) and [CBV](https://ref.gs1.org/standards/cbv/) | GS1 | Visibility events: what, when, where, why and how, with a shared vocabulary | [05-store](../lifecycle/05-store.md), [08-cross-cutting](../lifecycle/08-cross-cutting.md) |
| [DCSA eBL](https://dcsa.org/standards/bill-of-lading) | Digital Container Shipping Association | Electronic bill of lading and sea waybill | [08-cross-cutting](../lifecycle/08-cross-cutting.md) |
| [DCSA Track and Trace](https://dcsa.org/standards/track-and-trace) | DCSA | Container, transport and equipment events | [04-move](../lifecycle/04-move.md) |
| [DCSA Port Call](https://dcsa.org/standards/port-call) | DCSA | Port call timestamps for just-in-time arrival | [04-move](../lifecycle/04-move.md) |
| [e-CMR](https://unece.org/DAM/trans/conventn/e-CMRe.pdf) | UNECE (Additional Protocol to the CMR Convention) | Electronic road consignment note | [04-move](../lifecycle/04-move.md) |
| [eFTI Regulation](https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en) | European Union (Regulation (EU) 2020/1056) | Legal acceptance of electronic freight information by EU authorities | [04-move](../lifecycle/04-move.md) |
| [GHG Protocol Scope 3 Standard](https://ghgprotocol.org/corporate-value-chain-scope-3-standard) | GHG Protocol (WRI and WBCSD) | Corporate value chain emissions in 15 categories | [08-cross-cutting](../lifecycle/08-cross-cutting.md), [demo 02](../../implementations/02-scope3-spend-vs-activity), [demo 08](../../implementations/08-scope3-uncertainty) |
| [ISO 14083:2023](https://www.iso.org/standard/78864.html) | ISO (TC 207/SC 7) | Method for transport chain GHG emissions, all modes plus hubs | [08-cross-cutting](../lifecycle/08-cross-cutting.md), [KPIs](kpis.md) |
| [GLEC Framework](https://smartfreightcentre.org/news/13311209) | Smart Freight Centre (Global Logistics Emissions Council) | Practical guide for logistics emissions, aligned with ISO 14083 | [08-cross-cutting](../lifecycle/08-cross-cutting.md), [KPIs](kpis.md) |
| [PACT Methodology and Technical Specifications](https://www.carbon-transparency.org/) | Partnership for Carbon Transparency (WBCSD) | Product carbon footprints and how to exchange them between companies | [08-cross-cutting](../lifecycle/08-cross-cutting.md), [SCX-Bench](../../benchmark/README.md) |

## EDI: ANSI X12

X12 is the dominant EDI standard in North America. Each message is a numbered transaction set. Owner: [X12](https://x12.org/products/transaction-sets).

| Set | Name | Sent by, to | Use |
|---|---|---|---|
| 850 | Purchase Order | Buyer to seller | Places an order |
| 856 | Ship Notice/Manifest | Shipper to receiver | The advance ship notice (ASN): what is coming, packed how, often with SSCCs |
| 810 | Invoice | Seller to buyer | Bills for goods |
| 204 | Motor Carrier Load Tender | Shipper to carrier | Offers a load |
| 990 | Response to a Load Tender | Carrier to shipper | Accepts or declines the tender |
| 214 | Transportation Carrier Shipment Status Message | Carrier to shipper | Pickup, in-transit, arrival and delivery events |
| 210 | Motor Carrier Freight Details and Invoice | Carrier to shipper | Bills for freight, including accessorials such as detention |
| 997 | Functional Acknowledgment | Receiver to sender | Confirms a message was received and parsed, not that it was accepted as a business matter |

Notes:
- Partners agree an implementation guide per relationship. Two companies' 214s can use different status codes for the same event.
- 214 timestamps are often entered after the fact. Treat them as noisy labels when training ETA or dwell models.
- A 997 means "received", not "agreed". Agents must not treat it as confirmation of a tender or invoice.

## EDI: UN/EDIFACT

UN/EDIFACT is the United Nations EDI standard, developed by UN/CEFACT and published by UNECE in the UN Trade Data Interchange Directory. It is common in Europe, Asia, ocean shipping and customs. Owner: [UNECE](https://unece.org/trade/uncefact/introducing-unedifact).

| Message | Name | Rough X12 counterpart |
|---|---|---|
| ORDERS | Purchase order message | 850 |
| DESADV | Despatch advice message | 856 |
| INVOIC | Invoice message | 810 |
| IFTMIN | Instruction message (transport booking or instruction) | 204 |
| IFTSTA | International multimodal status report message | 214 |

The counterparts are approximate. The segment structure and code lists differ, so mapping between the two is real work.

## GS1 identifiers and EPCIS

GS1 is the global, not-for-profit standards body behind barcodes. Its identifiers are the shared keys most supply chain data joins on.

| Identifier | Identifies | Format | Owner page |
|---|---|---|---|
| GTIN | A trade item (product at a packaging level) | 8, 12, 13 or 14 digits | [GTIN](https://www.gs1.org/standards/id-keys/gtin) |
| SSCC | A logistic unit (one specific pallet, case or parcel) | 18 digits | [SSCC](https://www.gs1.org/standards/id-keys/sscc) |
| GLN | A legal entity, function or physical location | 13 digits | [GLN](https://www.gs1.org/standards/id-keys/gln) |
| GS1 Digital Link | Any GS1 key written as a web URI, so one QR code can serve scanning and web links | URI syntax | [GS1 Digital Link](https://www.gs1.org/standards/gs1-digital-link) |

[EPCIS](https://www.gs1.org/standards/epcis) (Electronic Product Code Information Services) is the GS1 standard for sharing visibility events within and between companies. [Release 2.0](https://ref.gs1.org/standards/epcis/) was ratified in June 2022 and added JSON and a REST interface alongside XML, plus sensor data. The [Core Business Vocabulary (CBV)](https://ref.gs1.org/standards/cbv/) gives shared values for fields such as business step (for example, shipping, receiving) and disposition (for example, in transit, damaged).

| EPCIS event type | Records |
|---|---|
| ObjectEvent | Something happened to one or more objects (observed, shipped, received) |
| AggregationEvent | Objects packed into or unpacked from a parent, such as cases onto an SSCC pallet |
| TransactionEvent | Objects linked to or unlinked from a business transaction, such as a purchase order |
| TransformationEvent | Inputs consumed to make outputs, as in production |
| AssociationEvent | Assets associated with each other, such as a sensor fitted to a container |

Why it matters for AI: EPCIS events are structured, timestamped and keyed on GS1 identifiers. They make good inputs for traceability, dwell and anomaly models, and give agents a clean record to reason over.

## Ocean: DCSA

The [Digital Container Shipping Association](https://dcsa.org/standards) publishes open, free standards for container shipping, set by its member carriers.

| Standard | Covers |
|---|---|
| [Bill of Lading (eBL)](https://dcsa.org/standards/bill-of-lading) | Electronic bill of lading and sea waybill data and process |
| [Track and Trace](https://dcsa.org/standards/track-and-trace) | Shipment, transport and equipment events for container visibility |
| [Port Call](https://dcsa.org/standards/port-call) | Port call event timestamps that let vessels adopt just-in-time arrival and slow down instead of waiting at anchor |
| Others on the [standards page](https://dcsa.org/standards) | Booking, commercial schedules, operational vessel schedules, arrival notice, verified gross mass, load list and bay plan |

eBL adoption was about 11% by mid-2025, and nine major carriers have committed to 100% by 2030 ([08-cross-cutting](../lifecycle/08-cross-cutting.md)). An original bill of lading is a document of title: whoever holds it can claim the cargo. That is why legal recognition, not file format, has been the bottleneck.

## Electronic freight documents: e-CMR and eFTI

| Instrument | What it does | Status |
|---|---|---|
| [e-CMR](https://unece.org/DAM/trans/conventn/e-CMRe.pdf) | Additional Protocol to the UN CMR Convention on international road carriage. Gives an electronic consignment note the same legal value as the paper CMR note, if it is authenticated with a reliable electronic signature and its integrity is assured. | In force since 2011, for states that have ratified it |
| [eFTI Regulation](https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en) | Regulation (EU) 2020/1056 on electronic freight transport information. Member State authorities must accept regulatory freight information that operators share electronically through certified eFTI platforms. Covers road, rail, inland waterway and air. | Applies in full from 9 July 2027 |

Why it matters for AI: once documents are structured data with legal standing, document AI moves from reading scans to validating fields, and agents can complete and share documents without a paper copy following.

## Emissions data

| Standard | Owner | Scope | Use |
|---|---|---|---|
| [GHG Protocol Corporate Value Chain (Scope 3) Standard](https://ghgprotocol.org/corporate-value-chain-scope-3-standard) | GHG Protocol | Company-level value chain emissions, 15 categories upstream and downstream | What to report. Transport appears as category 4 (upstream) and category 9 (downstream) transportation and distribution. |
| [ISO 14083:2023](https://www.iso.org/standard/78864.html) | ISO | Quantification and reporting of GHG emissions from transport chain operations, freight and passengers, all modes, including hubs | How to calculate transport emissions |
| [GLEC Framework](https://smartfreightcentre.org/news/13311209) | Smart Freight Centre | Logistics emissions calculation and reporting across road, rail, air, sea, inland waterways and hubs; version 3.2 published October 2025 | The practical implementation guide for ISO 14083, with default emission factors |
| [PACT Methodology](https://www.carbon-transparency.org/) (previously the Pathfinder Framework) and [Technical Specifications](https://wbcsd.github.io/data-exchange-protocol/v3/) | Partnership for Carbon Transparency (WBCSD) | Cradle-to-gate product carbon footprints, built on the GHG Protocol and ISO 14067, plus a data model and API for exchanging them | How a supplier sends a product footprint to a customer |

How they fit together: the GHG Protocol says what a company must count. ISO 14083 and the GLEC Framework say how to calculate the transport part. PACT says how to calculate a product footprint and send it between companies. An agent asking a supplier for "its footprint in the PACT format" ([SCX-Bench](../../benchmark/README.md)) is asking for a PACT data exchange record.

Pitfalls:
- Spend-based Scope 3 tracks invoices, not physical activity ([demo 02](../../implementations/02-scope3-spend-vs-activity)).
- A single footprint number hides wide uncertainty when much of it is modelled ([demo 08](../../implementations/08-scope3-uncertainty)).
- Transport emissions must state their boundary (well-to-wheel or tank-to-wheel) before they can be compared ([KPIs](kpis.md)).

## See also
- [KPI dictionary](kpis.md)
- [Glossary](../glossary.md)
- [Technology fit guide](../technology/fit-guide.md)
