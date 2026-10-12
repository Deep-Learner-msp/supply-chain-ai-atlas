# Learning path

Three ordered tracks: for an ML or LLM engineer new to supply chain, for a supply chain practitioner new to ML, and for a researcher. Each step pairs a page or demo in this repo with an outside resource.

Every outside resource below was checked in October 2026. "Free" means free to read or audit online at that time; course certificates usually cost money. Paid items are marked.

## Track A: ML or LLM engineer, new to supply chain

Goal: learn what the operation actually decides, then where models help and where they do not.

| Step | In this repo | Outside resource | You can now |
|---|---|---|---|
| 1. The shape of the system | [Lifecycle overview](../README.md#the-supply-chain-end-to-end), then [Plan](lifecycle/01-plan.md) to [Return](lifecycle/07-return.md) in order | MIT OpenCourseWare, [15.762J Supply Chain Planning](https://ocw.mit.edu/courses/15-762j-supply-chain-planning-spring-2011/) (free) | Name the decisions at each stage |
| 2. The vocabulary | [Glossary](glossary.md), [KPI dictionary](reference/kpis.md) | | Read an ops review without a translator |
| 3. Why supply chains overreact | [Demo 01 bullwhip](../implementations/01-bullwhip-simulator) | | Explain why sharing demand beats better forecasting at one tier |
| 4. Inventory basics | [Demo 09 safety stock](../implementations/09-safety-stock) | MITx MicroMasters in Supply Chain Management, [SC1x Supply Chain Fundamentals](https://learn.mit.edu/programs/program-v1:MITxT+SCM) (free to audit; certificate paid) | Size safety stock and know what the formula ignores |
| 5. Problem types | [Fit guide](technology/fit-guide.md) | | Say which problems an LLM should not solve |
| 6. Forecasting done properly | [Demo 03](../implementations/03-forecast-baselines), [demo 12](../implementations/12-eta-calibration) | Hyndman and Athanasopoulos, [Forecasting: Principles and Practice, 3rd ed.](https://otexts.com/fpp3/) (free), chapters on benchmarks, accuracy and cross-validation | Backtest against seasonal naive and check interval coverage |
| 7. Optimization | [Demo 04](../implementations/04-llm-solver-interface), [demo 05](../implementations/05-dock-scheduling), [demo 11](../implementations/11-changeover-scheduling) | [OR-Tools documentation](https://developers.google.com/optimization) (free), then Krupke's [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/) (free) | Write a small scheduling model and add a stability term |
| 8. Warehouses | [Store](lifecycle/05-store.md) | Bartholdi and Hackman, [Warehouse & Distribution Science](https://www.warehouse-science.com/) (free textbook) | Reason about slotting, picking and labour |
| 9. Messages and documents | [Data standards](reference/data-standards.md), [demo 13](../implementations/13-document-validation) | | Know what an EDI 214 or a BOL carries, and validate extracted fields |
| 10. Agents that hold up | [Agent architecture](playbooks/agent-architecture.md), [demo 06](../implementations/06-agent-with-guardrails), [SCX-Bench](../benchmark) | OWASP [Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) (free) | Build an agent with allowed tools, approvals and an audit log |
| 11. Evaluation and rollout | [Evaluation](playbooks/evaluation.md), [deploying AI](playbooks/deploying-ai.md) | | Design a shadow-mode pilot with a baseline and kill criteria |

## Track B: supply chain practitioner, new to ML

Goal: enough ML to judge a vendor pitch, run a pilot, and know when the answer is "not ML".

| Step | In this repo | Outside resource | You can now |
|---|---|---|---|
| 1. Name the problem type first | [Fit guide](technology/fit-guide.md) | | Sort a use case into prediction, planning, coordination, documents or shared truth |
| 2. ML fundamentals | | Google [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) (free) | Explain training, testing, overfitting and features |
| 3. Hands-on Python and ML | Run `make demos` from the [README](../README.md#quick-start) | [Kaggle Learn](https://www.kaggle.com/learn) (free short courses: Python, pandas, intro to ML) | Load data, fit a model, read the output |
| 4. Forecasting | [Demo 03](../implementations/03-forecast-baselines), [Plan](lifecycle/01-plan.md) | [FPP3](https://otexts.com/fpp3/) (free), chapters 1 to 5 | Ask any forecast vendor "what is your MASE against seasonal naive?" |
| 5. Uncertainty | [Demo 09](../implementations/09-safety-stock), [demo 12](../implementations/12-eta-calibration), [demo 08](../implementations/08-scope3-uncertainty) | [FPP3, prediction intervals](https://otexts.com/fpp3/prediction-intervals.html) (free) | Check whether a stated 95% really means 95% |
| 6. Optimization without the maths | [Demo 05](../implementations/05-dock-scheduling), [demo 10](../implementations/10-dual-sourcing), [demo 11](../implementations/11-changeover-scheduling) | [OR-Tools guides](https://developers.google.com/optimization) (free): routing and scheduling | Tell a solver problem from a prediction problem |
| 7. LLMs and agents | [Agent architecture](playbooks/agent-architecture.md), [demo 06](../implementations/06-agent-with-guardrails) | Hugging Face [AI Agents Course](https://huggingface.co/learn/agents-course) (free) | List what an agent may do alone and what needs approval |
| 8. Documents | [Demo 13](../implementations/13-document-validation) | | Ask for field-level accuracy and residual error, not "95% accurate" |
| 9. Running a pilot | [Deploying AI](playbooks/deploying-ai.md), [evaluation](playbooks/evaluation.md) | | Write a one-page pilot design with a baseline, a guardrail metric and a stop rule |
| 10. Go further | | James, Witten, Hastie and Tibshirani (Taylor joins for the Python edition), [An Introduction to Statistical Learning](https://www.statlearning.com/) (free PDF, R and Python editions) | Read ML papers and vendor white papers critically |

For a structured supply chain credential alongside this track, the [MITx MicroMasters in SCM](https://learn.mit.edu/programs/program-v1:MITxT+SCM) has five courses (SC0x Analytics, SC1x Fundamentals, SC2x Design, SC3x Dynamics, SC4x Technology and Systems). Auditing is free; the certificate track is paid.

## Track C: researcher

Goal: find a real problem, the right baselines and honest evaluation.

| Step | In this repo | Outside resource | You can now |
|---|---|---|---|
| 1. The research map | [Papers](../papers/2025-2026.md), [open problems](open-problems.md) | | Place your work in a line of research |
| 2. LLMs and OR | [Fit guide](technology/fit-guide.md), [demo 04](../implementations/04-llm-solver-interface) | [Large Language Models in Operations Research: Methods, Applications, and Challenges](https://arxiv.org/abs/2509.18180) (2025, free on arXiv) | Know what "LLM for optimization" has and has not shown |
| 3. Learning inside optimization | [Make](lifecycle/03-make.md), [Move](lifecycle/04-move.md) | Bengio, Lodi and Prouvost, [Machine Learning for Combinatorial Optimization: a Methodological Tour d'Horizon](https://arxiv.org/abs/1811.06128) (free on arXiv) | Frame a learned heuristic against a classical solver |
| 4. Sequential decisions under uncertainty | [Demo 01](../implementations/01-bullwhip-simulator), [demo 10](../implementations/10-dual-sourcing) | Powell, [Sequential Decision Analytics and Modeling](https://castle.princeton.edu/sdamodeling/) (2nd ed., free PDF); Sutton and Barto, [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) (2nd ed., free PDF) | Model inventory and dispatch as sequential decisions, with policies to compare |
| 5. Forecasting research | [Demo 03](../implementations/03-forecast-baselines), [demo 07](../implementations/07-federated-forecasting) | Petropoulos et al., [Forecasting: theory and practice](https://arxiv.org/abs/2012.03854) (free on arXiv) | Pick baselines a forecasting reviewer will accept |
| 6. Optimization modelling | [Demo 11](../implementations/11-changeover-scheduling) | [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/) (free); companion notebooks for Postek, Zocca, Gromicho and Kantor, [Hands-On Mathematical Optimization with Python](https://mobook.github.io/MO-book/intro.html) (notebooks free online; printed book paid); Boyd and Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/) (free PDF) | Build a model a practitioner can check |
| 7. Data | [Datasets](../datasets/README.md) | | Choose a public dataset and know its limits |
| 8. Agent evaluation | [SCX-Bench](../benchmark), [evaluation](playbooks/evaluation.md#agents) | [τ-bench](https://arxiv.org/abs/2406.12045) and [AgentDojo](https://arxiv.org/abs/2406.13352) (free on arXiv) | Report safe success, pass^k and injection results, not just task success |
| 9. Contribute | [CONTRIBUTING.md](../CONTRIBUTING.md) | | Add a task to SCX-Bench or a demo for an open problem |

## Libraries used along the way

| Library | Used for | Docs |
|---|---|---|
| OR-Tools | Routing, CP-SAT scheduling, linear programs | [developers.google.com/optimization](https://developers.google.com/optimization) |
| PyVRP | Vehicle routing | [pyvrp.org](https://pyvrp.org/) |
| statsforecast | Fast statistical forecasting baselines | [Nixtla statsforecast](https://nixtlaverse.nixtla.io/statsforecast/index.html) |
| stockpyl | Inventory models | [stockpyl.readthedocs.io](https://stockpyl.readthedocs.io/) |

More tools, filed by problem type, are in [repos](../repos/README.md).
