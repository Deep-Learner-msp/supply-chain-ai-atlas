# Glossary

Supply chain and AI terms used across this repo. Formulas for metrics are in the [KPI dictionary](reference/kpis.md); message and identifier standards are in [data standards](reference/data-standards.md).

| Term | Meaning |
|---|---|
| 3PL / 4PL | Third-party logistics provider runs logistics for you; a 4PL manages several 3PLs |
| ABC analysis | Ranking items by value or volume so the few that matter most (A items) get the closest control |
| Accessorial | A carrier charge on top of the line-haul rate, such as detention, liftgate or fuel surcharge |
| Agent | An AI system, usually an LLM, that decides its next step and calls tools to act, rather than only answering |
| ASN | Advance ship notice: a message telling the receiver what is coming and how it is packed (EDI 856, EDIFACT DESADV) |
| ATA / ATD | Actual time of arrival / actual time of departure |
| Backhaul | A load carried on the return leg of a trip, to avoid driving empty |
| Backorder | Demand that could not be filled from stock and will be filled later |
| Bias (forecast) | A forecast that is consistently too high or too low |
| BOL | Bill of lading: the document that travels with a shipment |
| BOM | Bill of materials: the parts and quantities that make up a product |
| Bonded warehouse | A warehouse where imported goods are stored before duties are paid |
| Bullwhip effect | Demand swings growing as they move upstream |
| Calibration | How well stated probabilities match outcomes: an 80% interval should contain about 80% of actuals |
| Capacity planning | Matching the people, machines and space you have to the work you expect |
| Carrier | The company that physically moves freight |
| Cash-to-cash cycle | Days between paying suppliers and being paid by customers: DIO plus DSO minus DPO |
| CBV | Core Business Vocabulary: GS1's shared values for EPCIS fields such as business step and disposition |
| Chain of thought | A model writing out intermediate reasoning steps before its answer |
| Chassis | The wheeled frame a shipping container sits on for road moves |
| CMR | The UN convention for international road carriage of goods, and its consignment note |
| COGS | Cost of goods sold |
| Cold chain | A temperature-controlled supply chain for food, medicine and other perishables |
| Conformal prediction | A method that wraps any model to give prediction intervals with a guaranteed coverage rate, assuming past and future data are exchangeable |
| Consolidation | Combining several small shipments into one larger one to cut cost |
| Constraint programming | Solving by stating rules that a solution must satisfy and letting a solver search; strong for scheduling |
| Cost to serve | The full cost of serving one customer or channel |
| CP-SAT | Google OR-Tools' constraint programming solver, built on SAT techniques; used in the [dock scheduling demo](../implementations/05-dock-scheduling) |
| Cross-docking | Moving goods from inbound to outbound trucks with little or no storage in between |
| CRPS | Continuous ranked probability score: scores a whole forecast distribution against the actual |
| Cycle count | Counting a small part of inventory often, instead of everything once a year |
| Cycle service level | Probability of not running out of stock during a replenishment cycle |
| Days of supply | How many days current inventory will last at expected demand |
| DC | Distribution centre |
| DCSA | Digital Container Shipping Association: sets open data standards for container shipping |
| Deadhead | Driving empty; see empty miles |
| Demand sensing | Short-term forecast updates from recent signals such as orders, point of sale data or weather |
| Demurrage | Charges when a container sits at a port or terminal beyond free time |
| Detention | Charges when a truck waits beyond the free time at a facility |
| Digital twin | A model of a real network or site, kept in sync with live data, used to test decisions before making them |
| Disposition | What happens to a returned or damaged item: restock, refurbish, liquidate, recycle or destroy |
| Dock-to-stock | Time from goods arriving at the dock to being put away and available |
| Document AI | Models that turn scans and PDFs into structured fields |
| Drayage | Short truck moves of containers between ports, rail yards and nearby facilities |
| Dwell time | Time a shipment or truck spends waiting at a location |
| e-CMR | The electronic version of the CMR road consignment note |
| eBL | Electronic bill of lading |
| EDI | Electronic data interchange: standard machine-readable business messages between companies |
| EDI 204 / 214 / 210 | Load tender / shipment status / freight invoice messages |
| EDIFACT | The United Nations EDI standard, used mostly outside North America |
| eFTI | The EU regulation requiring authorities to accept electronic freight transport information |
| ELD | Electronic logging device: records truck drivers' hours of service |
| Embedding | A list of numbers representing text or another object, so that similar things sit close together |
| Empty miles | Miles driven with no load, as a share of total miles |
| EOQ | Economic order quantity: the order size that balances ordering cost against holding cost |
| EPCIS | GS1 standard for sharing visibility events (what, when, where, why, how) within and between companies |
| ERP | Enterprise resource planning: the core system for orders, inventory and finance |
| ETA | Estimated time of arrival |
| Evaluation (evals) | A fixed set of test cases used to score a model or agent before and after changes |
| Federated learning | Training a shared model across several parties without moving their raw data; see the [federated demo](../implementations/07-federated-forecasting) |
| Fill rate | Share of demand shipped from stock on the first attempt |
| Fine-tuning | Further training of a pretrained model on your own data |
| First mile / last mile | The first leg of a shipment from origin / the final leg to the customer |
| Foundation model | A large model pretrained on broad data and reused for many tasks, such as an LLM or a time-series model like Chronos |
| Freight class | The US LTL classification that sets price by density, handling and liability |
| Freight forwarder | A company that arranges shipping on behalf of shippers, usually across borders and modes |
| FTL / LTL | Full truckload / less than truckload |
| GHG Protocol | The standards body and standards for corporate greenhouse gas accounting, including Scope 3 |
| GLEC Framework | Smart Freight Centre's method for calculating and reporting logistics emissions, aligned with ISO 14083 |
| GLN | Global Location Number: GS1 identifier for a party or location |
| Gradient-boosted trees | An ensemble of decision trees built one after another to fix earlier errors; a strong default for tabular prediction |
| Graph neural network | A neural network that learns over nodes and links, such as suppliers and lanes |
| GTIN | Global Trade Item Number: GS1 identifier for a product |
| Guardrail | A rule outside the model that limits what an agent may do, such as an allowed tool list or human approval on money |
| Hallucination | A model stating something false or unsupported as if it were fact |
| Hours of service | Rules limiting how long truck drivers may drive and work |
| Human in the loop | A person reviews or approves an AI decision before it takes effect |
| Incoterms | ICC trade terms that set who pays for and bears risk on each part of an international shipment |
| Intermittent demand | Demand with many zero periods; also called lumpy demand |
| Intermodal | Moving freight in one container across more than one mode, often truck and rail |
| Inventory turns | Cost of goods sold divided by average inventory |
| ISO 14083 | The international standard for calculating greenhouse gas emissions from transport chains |
| Knowledge graph | Facts stored as entities and relationships, such as supplier, part and site |
| Lane | An origin and destination pair that freight moves on |
| Lead time | Time from placing an order to receiving it |
| Learning to optimize | Using machine learning to speed up or guide optimization solvers |
| LLM | Large language model |
| Load tender | An offer of a load from a shipper to a carrier |
| Lot sizing | Deciding how much to produce or order at a time |
| MAPE | Mean absolute percentage error; breaks on zero or near-zero demand |
| MASE | Mean absolute scaled error: forecast error relative to a naive forecast |
| MCP | Model Context Protocol: an open protocol for connecting AI models to tools and data |
| MES | Manufacturing execution system: runs and records work on the factory floor |
| Milk run | A route that collects from or delivers to several stops in a fixed loop |
| MILP | Mixed-integer linear programming: optimization with linear constraints and some whole-number decisions |
| Mode | The type of transport: road, rail, ocean, air, inland waterway or parcel |
| MRP | Material requirements planning: turns a production plan and BOM into part orders |
| Nearshoring | Moving supply closer to the market it serves |
| OEE | Overall equipment effectiveness: availability times performance times quality |
| Optimality gap | How far a solver's best solution may be from the best possible one |
| OR-Tools | Google's open-source optimization toolkit for routing, scheduling and linear programs |
| OTIF | On time, in full: a delivery performance measure, often with retailer fines |
| PACT | Partnership for Carbon Transparency: method and data exchange standard for product carbon footprints |
| Pallet | A flat base that goods are stacked on for handling by forklift |
| Perfect order | An order delivered on time, complete, undamaged and with correct documents |
| Pinball loss | The standard score for a quantile forecast; also called quantile loss |
| POD | Proof of delivery |
| Postponement | Delaying final product configuration until demand is clearer |
| Prompt injection | Text in an input that tries to override an AI system's instructions |
| Purchase order (PO) | A buyer's formal order to a supplier |
| Put-away | Moving received goods into their storage location |
| RAG | Retrieval-augmented generation: fetching relevant documents and giving them to an LLM with the question |
| Reefer | A refrigerated trailer or container |
| Reinforcement learning | Learning a policy by trial and error against a reward signal |
| Reorder point | The stock level that triggers a new order |
| Reverse logistics | Moving goods back from customers for return, repair, reuse or recycling |
| RFID | Radio-frequency identification: tags read by radio rather than line of sight |
| Routing guide | A shipper's ranked list of carriers to tender each lane to |
| S&OP / IBP | Sales and operations planning / integrated business planning |
| Safety stock | Extra inventory held against uncertainty |
| SCAC | Standard Carrier Alpha Code: a two-to-four letter carrier code used in North America |
| Scope 1, 2, 3 | Direct emissions, purchased energy, and everything else in the value chain |
| SCOR | ASCM's reference model of supply chain processes and metrics |
| Seasonal naive | A forecast that repeats the value from the same period last season; the baseline to beat |
| Shipper | The company that owns the goods and buys transport |
| Simulation | Running a model of a system many times to see how it behaves under uncertainty |
| SKU | Stock keeping unit: one distinct item as stocked, often one product in one location |
| Slotting | Choosing which storage location each item goes in |
| Spot rate / contract rate | Price for a single load now / price agreed for a lane over a period |
| SSCC | Serial Shipping Container Code: GS1 identifier for one pallet, case or parcel |
| Stock-out | Running out of an item when there is demand for it |
| Supplier risk | The chance that a supplier fails to deliver because of finance, disruption or compliance problems |
| Synthetic data | Artificially generated data used to train or test models when real data is scarce or private |
| Tender acceptance | Share of offered loads a carrier accepts |
| Time-series foundation model | A model pretrained on many time series that forecasts new series with little or no training, such as Chronos, TimesFM or Moirai |
| TMS / WMS / YMS | Transportation / warehouse / yard management system |
| Tool calling | An LLM producing a structured request for a function, which the host system runs |
| Track and trace | Recording and sharing where a shipment or container is and what has happened to it |
| Transloading | Moving goods from one container or vehicle to another, often between modes |
| Uncertainty quantification | Giving a range or distribution with a prediction, not only one number |
| Vendor-managed inventory (VMI) | The supplier decides when to replenish the customer's stock |
| VRP | Vehicle routing problem: assign stops to vehicles and order them to minimize cost under constraints |
| WAPE | Weighted absolute percentage error: total absolute error over total actual demand |
| Wave picking | Releasing orders to the warehouse floor in planned batches |
| WISMO | "Where is my order?" customer enquiries |
| Yard | The area outside a facility where trailers and containers wait |
| Zero-shot | Using a model on a task or series it was not trained on, with no examples |
