# Open-source tools

Filed by problem type. Star counts change: check the repo. Every repo below was checked in October 2026: public, not archived. Repos with no push in the last 18 months are marked *Inactive* and kept only where they are still a useful reference.

## Contents
[Solvers and modelling](#optimization-and-routing) · [Routing engines](#routing-engines-and-road-networks) · [LLMs for optimization](#llms-for-optimization-and-heuristic-design) · [Forecasting](#forecasting) · [Forecast evaluation](#forecast-evaluation-and-uncertainty) · [Inventory and simulation](#inventory-and-simulation) · [Warehouse](#warehouse-and-multi-robot-path-finding) · [Documents](#document-ai) · [Graphs and sustainability](#graphs-and-sustainability) · [Systems](#open-source-systems) · [Related lists](#related-lists)

## Optimization and routing
| Repo | What it is |
|---|---|
| [google/or-tools](https://github.com/google/or-tools) | Google's solver suite: routing, scheduling, MILP, CP-SAT |
| [PyVRP/PyVRP](https://github.com/PyVRP/PyVRP) | State-of-the-art vehicle routing solver in Python |
| [VROOM-Project/vroom](https://github.com/VROOM-Project/vroom) | Fast vehicle routing engine (C++) with time windows, capacities and skills; pairs with OSRM or Valhalla |
| [reinterpretcat/vrp](https://github.com/reinterpretcat/vrp) | Rich vehicle routing solver in Rust, with a JSON problem format |
| [graphhopper/jsprit](https://github.com/graphhopper/jsprit) | Java toolkit for rich vehicle routing problems |
| [TimefoldAI/timefold-solver](https://github.com/TimefoldAI/timefold-solver) | Java and Kotlin planning solver for routing, shift scheduling and maintenance planning |
| [ai4co/rl4co](https://github.com/ai4co/rl4co) | Reinforcement learning for combinatorial optimization |
| [ai4co/routefinder](https://github.com/ai4co/routefinder) | RouteFinder: one neural model trained across many VRP variants |
| [coin-or/pulp](https://github.com/coin-or/pulp) | Simple linear programming modelling in Python |
| [Pyomo/pyomo](https://github.com/Pyomo/pyomo) | Algebraic modelling for optimization |
| [cvxpy/cvxpy](https://github.com/cvxpy/cvxpy) | Python modelling language for convex optimization |
| [ERGO-Code/HiGHS](https://github.com/ERGO-Code/HiGHS) | Open-source LP and MIP solver; the default MILP backend in SciPy |
| [scipopt/PySCIPOpt](https://github.com/scipopt/PySCIPOpt) | Python interface to the SCIP MIP and constraint solver |
| [Gurobi/gurobi-optimods](https://github.com/Gurobi/gurobi-optimods) | Ready-made, data-driven APIs for common optimization tasks (needs a Gurobi licence to run) |
| [microsoft/OptiGuide](https://github.com/microsoft/OptiGuide) | LLM interface to supply chain optimization |
| [d-krupke/cpsat-primer](https://github.com/d-krupke/cpsat-primer) | The best hands-on guide to OR-Tools CP-SAT for scheduling |
| [OptimizationExpert/Pyomo](https://github.com/OptimizationExpert/Pyomo) | Library of solved supply chain models in Pyomo |
| [hzjken/multimodal-transportation-optimization](https://github.com/hzjken/multimodal-transportation-optimization) | Multi-modal transport cost minimization. *Inactive since 2020* |
| [samirsaci/supply-chain-optimization](https://github.com/samirsaci/supply-chain-optimization) | Network optimization tutorials with PuLP |
| [samirsaci/picking-route](https://github.com/samirsaci/picking-route) | Warehouse order batching and picking routes |

## Routing engines and road networks
| Repo | What it is |
|---|---|
| [Project-OSRM/osrm-backend](https://github.com/Project-OSRM/osrm-backend) | Open Source Routing Machine: fast shortest paths and distance matrices on OpenStreetMap |
| [valhalla/valhalla](https://github.com/valhalla/valhalla) | OpenStreetMap routing engine with truck costing, isochrones and map matching |
| [gboeing/osmnx](https://github.com/gboeing/osmnx) | Download and analyse street networks from OpenStreetMap in Python |

## LLMs for optimization and heuristic design
| Repo | What it is |
|---|---|
| [Cardinal-Operations/ORLM](https://github.com/Cardinal-Operations/ORLM) | ORLM: open LLMs trained for optimization modelling, with the IndustryOR benchmark |
| [antgroup/LLMOPT](https://github.com/antgroup/LLMOPT) | LLMOPT: model, data and training code for turning problem text into solver code |
| [optsuite/OptMATH](https://github.com/optsuite/OptMATH) | OptMATH: synthetic data generation for optimization modelling |
| [teshnizi/OptiMUS](https://github.com/teshnizi/OptiMUS) | OptiMUS: LLM agent that formulates and solves MILP models |
| [Optima-CityU/LLM4AD](https://github.com/Optima-CityU/LLM4AD) | Platform for LLM-driven algorithm design, with optimization tasks such as scheduling |
| [FeiLiu36/EoH](https://github.com/FeiLiu36/EoH) | Evolution of Heuristics: LLMs evolve heuristics for TSP, bin packing and more |
| [ai4co/reevo](https://github.com/ai4co/reevo) | ReEvo: LLMs as hyper-heuristics with reflective evolution |

## Forecasting
| Repo | What it is |
|---|---|
| [amazon-science/chronos-forecasting](https://github.com/amazon-science/chronos-forecasting) | Chronos, Chronos-Bolt and Chronos-2 time-series foundation models |
| [google-research/timesfm](https://github.com/google-research/timesfm) | TimesFM foundation forecaster |
| [SalesforceAIResearch/uni2ts](https://github.com/SalesforceAIResearch/uni2ts) | Moirai models |
| [DataDog/toto](https://github.com/DataDog/toto) | Toto foundation model and the BOOM observability benchmark |
| [thuml/Sundial](https://github.com/thuml/Sundial) | Sundial foundation models: generative forecasts from a flow-matching (TimeFlow) loss |
| [NX-AI/tirex](https://github.com/NX-AI/tirex) | TiRex: xLSTM-based zero-shot forecaster |
| [PriorLabs/tabpfn-time-series](https://github.com/PriorLabs/tabpfn-time-series) | Zero-shot forecasting with the TabPFN tabular foundation model |
| [TimeCopilot/timecopilot](https://github.com/TimeCopilot/timecopilot) | Forecasting agent that combines LLMs with foundation and statistical models |
| [Nixtla/statsforecast](https://github.com/Nixtla/statsforecast) | Fast statistical baselines |
| [Nixtla/neuralforecast](https://github.com/Nixtla/neuralforecast) | Neural forecasting models |
| [Nixtla/mlforecast](https://github.com/Nixtla/mlforecast) | Gradient-boosting forecasting at scale (LightGBM, XGBoost) |
| [Nixtla/hierarchicalforecast](https://github.com/Nixtla/hierarchicalforecast) | Hierarchical reconciliation (SKU, store, region) |
| [unit8co/darts](https://github.com/unit8co/darts) | One API over classical, ML and foundation forecasters |
| [sktime/sktime](https://github.com/sktime/sktime) | Unified framework for time-series learning, including forecasting pipelines |
| [awslabs/gluonts](https://github.com/awslabs/gluonts) | Probabilistic time-series models (DeepAR and others) |
| [autogluon/autogluon](https://github.com/autogluon/autogluon) | AutoML, including AutoGluon-TimeSeries ensembles |
| [facebook/prophet](https://github.com/facebook/prophet) | Additive model for series with strong seasonality and holidays |
| [thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library) | Reference implementations of many deep time-series models |

## Forecast evaluation and uncertainty
| Repo | What it is |
|---|---|
| [SalesforceAIResearch/gift-eval](https://github.com/SalesforceAIResearch/gift-eval) | GIFT-Eval benchmark and leaderboard code for general forecasting models |
| [autogluon/fev](https://github.com/autogluon/fev) | Forecast evaluation library behind fev-bench |
| [scikit-learn-contrib/MAPIE](https://github.com/scikit-learn-contrib/MAPIE) | Conformal prediction intervals, including for time series |

## Inventory and simulation
| Repo | What it is |
|---|---|
| [LarrySnyder/stockpyl](https://github.com/LarrySnyder/stockpyl) | Inventory optimization models in Python |
| [salabim/salabim](https://github.com/salabim/salabim) | Discrete-event simulation in Python, with animation; good for warehouse and yard models |
| [hubbs5/or-gym](https://github.com/hubbs5/or-gym) | RL environments for supply chain and OR problems. *Inactive since 2023* |
| [frenkowski/SCIMAI-Gym](https://github.com/frenkowski/SCIMAI-Gym) | Inventory management with deep RL and classic policies. *Inactive since 2024* |
| [OptMLGroup/DeepBeerInventory-RL](https://github.com/OptMLGroup/DeepBeerInventory-RL) | Deep RL agent for the beer game (bullwhip). *Inactive since 2023* |

## Warehouse and multi-robot path finding
| Repo | What it is |
|---|---|
| [Kei18/lacam3](https://github.com/Kei18/lacam3) | LaCAM*: real-time, large-scale multi-agent path finding |
| [CognitiveAISystems/MAPF-GPT](https://github.com/CognitiveAISystems/MAPF-GPT) | MAPF-GPT: transformer path finder trained by imitation learning |
| [Cognitive-AI-Systems/pogema](https://github.com/Cognitive-AI-Systems/pogema) | POGEMA: grid environment and benchmark for multi-agent path finding |
| [MAPF-Competition/Start-Kit](https://github.com/MAPF-Competition/Start-Kit) | Start kit for the League of Robot Runners warehouse robot competition |
| [open-rmf/rmf_ros2](https://github.com/open-rmf/rmf_ros2) | Open-RMF: fleet management and traffic control for mixed robot fleets |

## Document AI
| Repo | What it is |
|---|---|
| [docling-project/docling](https://github.com/docling-project/docling) | Converts PDFs and scans (invoices, bills of lading, rate sheets) into structured text and tables |
| [Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) | Document parsing and chunking for LLM pipelines |
| [mindee/doctr](https://github.com/mindee/doctr) | Deep learning OCR: text detection and recognition |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | Multilingual OCR and document structure toolkit |

## Graphs and sustainability
| Repo | What it is |
|---|---|
| [ciol-researchlab/SupplyGraph](https://github.com/ciol-researchlab/SupplyGraph) | Benchmark dataset for supply chain planning with graph neural networks. *No push since January 2025* |
| [samirsaci/supply-chain-sustainability](https://github.com/samirsaci/supply-chain-sustainability) | CO2 reporting for distribution networks in Python |
| [brightway-lca/brightway25](https://github.com/brightway-lca/brightway25) | Brightway life cycle assessment framework in Python |
| [mlco2/codecarbon](https://github.com/mlco2/codecarbon) | Measures the emissions of the compute your models use |

## Open-source systems
| Repo | What it is |
|---|---|
| [fleetbase/fleetbase](https://github.com/fleetbase/fleetbase) | Modular open-source logistics and supply chain operating system |
| [openboxes/openboxes](https://github.com/openboxes/openboxes) | Warehouse and inventory management system, built for healthcare supply chains |
| [frappe/erpnext](https://github.com/frappe/erpnext) | Open-source ERP with stock, purchasing and manufacturing modules |
| [karrioapi/karrio](https://github.com/karrioapi/karrio) | Self-hosted shipping API: labels, rates and tracking across carriers |
| [eclipse-ditto/ditto](https://github.com/eclipse-ditto/ditto) | Eclipse Ditto: framework for building digital twins of devices and assets |

## Related lists
| Repo | Scope |
|---|---|
| [FeiLiu36/LLM4AlgorithmDesign](https://github.com/FeiLiu36/LLM4AlgorithmDesign) | LLMs for optimization (formerly LLM4Opt) |
| [ai4co/awesome-fm4co](https://github.com/ai4co/awesome-fm4co) | Foundation models for combinatorial optimization |
| [Funkmyster/awesome-supply-chain](https://github.com/Funkmyster/awesome-supply-chain) | General supply chain blogs, podcasts and standards. *Inactive since 2023* |
| [Alro10/deep-learning-time-series](https://github.com/Alro10/deep-learning-time-series) | Deep learning for time-series forecasting. *Inactive since 2024* |
