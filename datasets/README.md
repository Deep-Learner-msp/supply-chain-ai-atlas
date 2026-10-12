# Datasets and benchmarks

Public data for forecasting, routing, scheduling, warehouse, document and emissions work. Links were checked in October 2026. A licence is listed only where we read it on the source page; otherwise it says "See source", and you should check before use, especially for commercial work.

## Forecasting and demand
| Dataset | Problem | Where | Licence |
|---|---|---|---|
| M5 Forecasting (Walmart) | Hierarchical retail demand, 42,840 series | [Kaggle: M5 Forecasting - Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy) | See source |
| Corporación Favorita | Grocery sales with promotions, holidays and oil prices | [Kaggle: Favorita Grocery Sales Forecasting](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting) | See source |
| Rossmann Store Sales | Daily store sales with promotions and competition | [Kaggle: Rossmann Store Sales](https://www.kaggle.com/competitions/rossmann-store-sales) | See source |
| GIFT-Eval | Benchmark for general forecasting models across domains and frequencies | [Hugging Face: Salesforce/GiftEval](https://huggingface.co/datasets/Salesforce/GiftEval) | Apache-2.0 |
| fev-bench | Forecasting benchmark with covariates, used by the fev library | [Hugging Face: autogluon/fev_datasets](https://huggingface.co/datasets/autogluon/fev_datasets) | Mixed, per dataset |
| Chronos datasets | Public time-series collection used to train and test Chronos | [Hugging Face: autogluon/chronos_datasets](https://huggingface.co/datasets/autogluon/chronos_datasets) | Mixed, per dataset |
| LOTSA | Large open pre-training archive for time-series foundation models (Moirai) | [Hugging Face: Salesforce/lotsa_data](https://huggingface.co/datasets/Salesforce/lotsa_data) | Apache-2.0 |

## Orders, shipping and last mile
| Dataset | Problem | Where | Licence |
|---|---|---|---|
| DataCo Smart Supply Chain | Orders, shipping, delays | [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) | See source |
| Olist Brazilian E-Commerce | Orders, delivery times, reviews | [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | See source |
| Amazon Last Mile Routing Research Challenge | Real driver routes, with stops, packages and time windows | [Registry of Open Data on AWS](https://registry.opendata.aws/amazon-last-mile-challenges/) | CC BY-NC 4.0 |
| LaDe | Last-mile pickup and delivery records from Cainiao, for ETA and route prediction | [Hugging Face: Cainiao-AI/LaDe](https://huggingface.co/datasets/Cainiao-AI/LaDe) | Apache-2.0 |
| AIS vessel traffic (US waters) | Ship positions for port, ocean ETA and congestion work | [Marine Cadastre: Vessel Traffic](https://hub.marinecadastre.gov/pages/vesseltraffic) | See source |

## Routing and scheduling instances
| Dataset | Problem | Where | Licence |
|---|---|---|---|
| CVRPLIB | Capacitated vehicle routing instances | [vrp.galgos.inf.puc-rio.br](http://vrp.galgos.inf.puc-rio.br/index.php/en/) | See source |
| Solomon and Gehring-Homberger VRPTW instances | Routing with time windows | [SINTEF TOP: VRPTW](https://www.sintef.no/projectweb/top/vrptw/) | See source |
| JSPLIB | Job-shop scheduling instances with best known bounds | [tamy0612/JSPLIB](https://github.com/tamy0612/JSPLIB) | See source |
| Starjob | LLM job-shop scheduling | [arXiv 2503.01877](https://arxiv.org/abs/2503.01877) | See source |

## Warehouse and multi-robot
| Dataset | Problem | Where | Licence |
|---|---|---|---|
| MovingAI MAPF benchmarks | Standard grid maps and scenarios, including warehouse layouts | [movingai.com](https://www.movingai.com/benchmarks/mapf.html) | See source |
| League of Robot Runners | Warehouse-style lifelong path finding and task assignment competition | [MAPF-Competition/Start-Kit](https://github.com/MAPF-Competition/Start-Kit) | MIT (start kit) |

## Documents
| Dataset | Problem | Where | Licence |
|---|---|---|---|
| DocILE | Key information and line-item extraction from business documents (mostly invoices) | [rossumai/docile](https://github.com/rossumai/docile) | MIT (code); see source for data terms |
| CORD | Receipt parsing with labelled fields | [clovaai/cord](https://github.com/clovaai/cord) | CC BY 4.0 |
| FUNSD | Form understanding on noisy scanned documents | [guillaumejaume.github.io/FUNSD](https://guillaumejaume.github.io/FUNSD/) | See source |

## Graphs and emissions
| Dataset | Problem | Where | Licence |
|---|---|---|---|
| SupplyGraph | Graph-based supply chain planning | [ciol-researchlab/SupplyGraph](https://github.com/ciol-researchlab/SupplyGraph) | LGPL-2.1 (repo) |
| Corporate emission reports | Extracting Scope 1/2/3 from sustainability reports (LLM fine-tuning) | [nopperl/corporate_emission_reports](https://github.com/nopperl/corporate_emission_reports), data on [Hugging Face](https://huggingface.co/datasets/nopperl/corporate-emission-reports) | Apache-2.0 (code), PDDL (data) |
| US EPA supply chain GHG emission factors | Spend-based emission factors by NAICS code, for Scope 3 estimates | [data.gov catalog](https://catalog.data.gov/dataset/supply-chain-greenhouse-gas-emission-factors-v1-3-by-naics-6) | See source |
| EXIOBASE | Multi-regional input-output tables with environmental extensions | [exiobase.eu](https://exiobase.eu/) | See source |
| Climate TRACE | Facility and sector-level emissions estimates, including shipping and road transport | [climatetrace.org/data](https://climatetrace.org/data) | See source |

Missing a dataset? Open a pull request with its licence and a one-line description.
