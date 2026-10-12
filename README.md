<p align="center"><img src="assets/banner.png" alt="Supply Chain AI Atlas" width="100%"></p>

<h3 align="center">Every supply chain problem, the technology that actually fits it, and what is still unsolved.</h3>

<p align="center">
  70+ papers from 2025 and 2026 &nbsp;·&nbsp; 25+ open-source tools &nbsp;·&nbsp; 8 runnable demos &nbsp;·&nbsp; SCX-Bench for supply chain agents
</p>

<p align="center">
  <a href="https://github.com/Deep-Learner-msp/supply-chain-ai-atlas/stargazers"><img src="https://img.shields.io/github/stars/Deep-Learner-msp/supply-chain-ai-atlas?style=flat&logo=github&color=F2A93B" alt="stars"></a>
  <a href="https://github.com/Deep-Learner-msp/supply-chain-ai-atlas/actions"><img src="https://github.com/Deep-Learner-msp/supply-chain-ai-atlas/actions/workflows/tests.yml/badge.svg" alt="tests"></a>
  <img src="https://img.shields.io/badge/papers-70%2B-F2A93B" alt="papers">
  <img src="https://img.shields.io/badge/runnable%20demos-8-5CC6A0" alt="demos">
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white" alt="python">
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-5CC6A0" alt="PRs welcome"></a>
  <a href="https://www.linkedin.com/in/mspraja"><img src="https://img.shields.io/badge/follow-LinkedIn-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <img src="https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-9FB0C6" alt="license">
</p>

<p align="center">
  <a href="#quick-start"><b>Quick start</b></a> &nbsp;·&nbsp;
  <a href="#runnable-demos"><b>Demos</b></a> &nbsp;·&nbsp;
  <a href="#scx-bench-a-benchmark-for-supply-chain-agents"><b>SCX-Bench</b></a> &nbsp;·&nbsp;
  <a href="papers/2025-2026.md"><b>Papers</b></a> &nbsp;·&nbsp;
  <a href="repos/README.md"><b>Tools</b></a> &nbsp;·&nbsp;
  <a href="docs/open-problems.md"><b>Open problems</b></a> &nbsp;·&nbsp;
  <a href="#contributing"><b>Contribute</b></a>
</p>

<p align="center"><sub><i>Physical supply chains and logistics, not software supply chain security.</i></sub></p>

---

## Why this exists

Most supply chain AI content is vendor marketing or generic AI hype. This repo sits in between.

<table>
<tr>
<td width="33%" valign="top">

**Problem first**

Organised by what a supply chain actually does: plan, source, make, move, store, deliver, return. The technology comes second.

</td>
<td width="33%" valign="top">

**Honest verdicts**

When an LLM is the wrong tool, the guide says so. Same for blockchain, digital twins and quantum. Name the problem type, then pick the tool.

</td>
<td width="33%" valign="top">

**Code you can run**

Eight demos and a benchmark, all on a laptop, about a minute end to end. Each one teaches a single thing that surprises people.

</td>
</tr>
</table>

<p align="center"><img src="assets/bullwhip.gif" alt="Bullwhip effect animation" width="80%"></p>
<p align="center"><sub>A 5% bump in shopper demand becomes an 80% swing at the supplier. <a href="implementations/01-bullwhip-simulator">Run it yourself.</a></sub></p>

## Quick start

```bash
git clone https://github.com/Deep-Learner-msp/supply-chain-ai-atlas.git
cd supply-chain-ai-atlas
pip install -r requirements.txt
make demos      # all eight demos and the benchmark, about a minute
```

Prefer the browser? Every demo has a Colab notebook: see the [demo table](#runnable-demos).

<details>
<summary><b>What you will see</b> (real output from <code>make demos</code>)</summary>

```text
=== implementations/01-bullwhip-simulator/simulate.py
Tier          No sharing   Sharing POS
Store               8.8%          8.8%
DC                 15.3%         12.5%
Brand              34.5%         16.2%
Supplier           80.4%         20.0%

=== implementations/02-scope3-spend-vs-activity/compare.py
Anita goes solar  : real -50% | reported +5%
Switch to coal    : real +140% | reported -10%
The spend-based number tracks the invoice, not the factory.

=== implementations/08-scope3-uncertainty/uncertainty.py
Single number most reports show : 5,190 t CO2e
Honest range (90%)              : 3,960 to 7,288 t  (median 4,946)

=== benchmark/run.py
SCX-Bench v0: 8 tasks
Agent                   Success  Violations  Safe success  Avg steps
do-nothing                 1/8           0          1/8        1.0
eager                      1/8           8          0/8        6.0
careful (rule-based)       8/8           0          8/8        4.2
```

</details>

## The supply chain, end to end

```mermaid
flowchart LR
    P[Plan<br/>demand, inventory, S&OP] --> S[Source<br/>suppliers, procurement]
    S --> M[Make<br/>production, scheduling]
    M --> T[Move<br/>transport, routing]
    T --> W[Store<br/>warehouse, yard, dock]
    W --> D[Deliver<br/>last mile, customer service]
    D --> R[Return<br/>reverse logistics]
    R -.-> P
```

| Stage | Core decisions | Demos | Read |
|---|---|---|---|
| **Plan** | How much will sell, how much to hold | 01, 03, 04, 07 | [01-plan](docs/lifecycle/01-plan.md) |
| **Source** | Which supplier, at what price and risk | | [02-source](docs/lifecycle/02-source.md) |
| **Make** | What to produce, when, on which line | | [03-make](docs/lifecycle/03-make.md) |
| **Move** | Which carrier, route and mode | 04, 06 | [04-move](docs/lifecycle/04-move.md) |
| **Store** | Which door, slot and shift | 05 | [05-store](docs/lifecycle/05-store.md) |
| **Deliver** | Last-mile route, promise date, customer updates | 06 | [06-deliver](docs/lifecycle/06-deliver.md) |
| **Return** | Restock, refurbish, recycle or scrap | | [07-return](docs/lifecycle/07-return.md) |
| **Cross-cutting** | Risk, Scope 3, data sharing | 02, 07, 08 | [08-cross-cutting](docs/lifecycle/08-cross-cutting.md) |

## Which technology fits which problem

> **Name the type of problem before you pick the tool.**

| Problem type | How to recognise it | Reach for | Common mistake |
|---|---|---|---|
| **Prediction** | A number you can score later | Forecasting models, time-series foundation models | Asking an LLM to guess the number |
| **Planning** | Hard constraints and a cost | Solvers, with an LLM as the interface | Letting the LLM write the plan |
| **Coordination** | Messages and judgment across companies | LLM agents with guardrails | Another dashboard |
| **Documents** | Paper that should be data | Document AI plus validation rules | Unchecked LLM reads |
| **Shared truth** | Parties who must agree or pool data | Standards, federated learning | Blockchain by default |

The full guide has honest verdicts on agents, foundation models, federated learning, digital twins, blockchain and quantum: **[docs/technology/fit-guide.md](docs/technology/fit-guide.md)**.

## Runnable demos

Each runs in under a minute and teaches one thing that surprises people.

| # | Demo | The lesson | Run |
|---|---|---|---|
| 01 | [Bullwhip simulator](implementations/01-bullwhip-simulator) | A 5% demand bump becomes an 80% swing at the supplier. Sharing demand data cuts it to 20% | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/01-bullwhip-simulator.ipynb) |
| 02 | [Scope 3: spend vs activity](implementations/02-scope3-spend-vs-activity) | A supplier halves its emissions and looks 5% worse on paper | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/02-scope3-spend-vs-activity.ipynb) |
| 03 | [Forecast baselines](implementations/03-forecast-baselines) | The most accurate model had poorly calibrated intervals | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/03-forecast-baselines.ipynb) |
| 04 | [LLM as solver interface](implementations/04-llm-solver-interface) | The LLM translates the question; the solver makes the plan | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/04-llm-solver-interface.ipynb) |
| 05 | [Dock scheduling](implementations/05-dock-scheduling) | The optimal re-plan moved 7 trucks; the stable one moved 1 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/05-dock-scheduling.ipynb) |
| 06 | [Agent with guardrails](implementations/06-agent-with-guardrails) | Allowed tools, approval on money, an audit log, a step limit | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/06-agent-with-guardrails.ipynb) |
| 07 | [Federated forecasting](implementations/07-federated-forecasting) | Shared models blur the partner who sees the shock first | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/07-federated-forecasting.ipynb) |
| 08 | [Scope 3 uncertainty](implementations/08-scope3-uncertainty) | One supplier caused 85% of the uncertainty, and it wasn't the biggest | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/08-scope3-uncertainty.ipynb) |

## SCX-Bench: a benchmark for supply chain agents

Agent benchmarks usually score whether the task got done. In supply chains, an agent that issues a refund to close a ticket "succeeded" and still lost money.

**[SCX-Bench](benchmark) ranks agents on safe success: the goal reached with zero policy violations.**

| Agent | Success | Violations | Safe success |
|---|:---:|:---:|:---:|
| do-nothing | 1/8 | 0 | 1/8 |
| eager (takes the money shortcut) | 1/8 | **8** | **0/8** |
| careful (rule-based reference) | 8/8 | 0 | **8/8** |

**Can your LLM agent beat the rule-based reference?** Write one function and add it to [`benchmark/run.py`](benchmark/run.py):

```python
def my_agent(goal, allowed, state, memory):
    # look at the goal and the world, pick one tool call
    return {"tool": "lookup_shipment", "args": {...}}
```

Eight tasks across documents, coordination, disputes, supplier data and customer service, each with one trap: an action that looks helpful but is wrong. Details in [benchmark/README.md](benchmark/README.md).

## Research and tools

<table>
<tr>
<td width="50%" valign="top">

### [70+ papers, 2025 to 2026](papers/2025-2026.md)
Agents, forecasting, optimization, routing, warehouse robotics, procurement negotiation, risk, Scope 3, federated learning and quantum. Each has one line on why it matters.

</td>
<td width="50%" valign="top">

### [25+ open-source tools](repos/README.md)
OR-Tools, PyVRP, Chronos, TimesFM, Moirai, Nixtla, stockpyl, or-gym, OptiGuide and more, filed by problem type.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [Datasets and benchmarks](datasets/README.md)
M5, DataCo, Olist, CVRPLIB, SupplyGraph, Starjob.

</td>
<td width="50%" valign="top">

### [Open problems](docs/open-problems.md)
Ten unsolved problems worth a thesis or a startup.

</td>
</tr>
</table>

## Start here

| If you are... | Start with |
|---|---|
| New to supply chain | [Start here](docs/00-start-here.md), then the lifecycle pages in order |
| An ML or LLM engineer | [Fit guide](docs/technology/fit-guide.md), demos 03, 04 and 06, then the [papers](papers/2025-2026.md) |
| Building agents | [Demo 06](implementations/06-agent-with-guardrails) and [SCX-Bench](benchmark) |
| A researcher | [Open problems](docs/open-problems.md) and [datasets](datasets/README.md) |
| A practitioner | The "Open problems" section of each lifecycle page |

## How this differs from other lists

| | General supply chain lists | AI-for-optimization lists | **This repo** |
|---|:---:|:---:|:---:|
| Organised by supply chain stage | ✅ | ❌ | ✅ |
| Which technology fits which problem | ❌ | ❌ | ✅ |
| 2025 to 2026 AI research | ❌ | ✅ | ✅ |
| Runnable demos | ❌ | ❌ | **8** |
| Benchmark for agents | ❌ | ❌ | **SCX-Bench** |
| Open problems | ❌ | ❌ | ✅ |

It complements them. See [related lists](repos/README.md#related-lists).

## Roadmap

Next up: a time-series foundation model vs baselines on M5, document AI for bills of lading, returns disposition, SCX-Bench v0.2 with 30 tasks and an LLM agent entry, and a monthly new-papers update. See [ROADMAP.md](ROADMAP.md).

## Contributing

Papers, tools, datasets, demos and benchmark tasks are all welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md). Every pull request runs the tests and checks every link.

## Cite

```bibtex
@misc{supplychainaiatlas2026,
  author = {MSP Raja},
  title  = {Supply Chain AI Atlas},
  year   = {2026},
  url    = {https://github.com/Deep-Learner-msp/supply-chain-ai-atlas}
}
```

Or use **Cite this repository** in the sidebar ([CITATION.cff](CITATION.cff)).

## Star history

<a href="https://star-history.com/#Deep-Learner-msp/supply-chain-ai-atlas&Date">
  <img src="https://api.star-history.com/svg?repos=Deep-Learner-msp/supply-chain-ai-atlas&type=Date" alt="Star history chart" width="70%">
</a>

## License

Text and diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: MIT. See [LICENSE](LICENSE).

---

<p align="center">
  Maintained by <a href="https://www.mspraja.com"><b>MSP Raja</b></a>.<br>
  If this saved you a week of reading, <b>a ⭐ helps other people find it.</b>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/mspraja"><img src="https://img.shields.io/badge/LinkedIn-MSP%20Raja-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://www.mspraja.com"><img src="https://img.shields.io/badge/Website-mspraja.com-111111?logo=googlechrome&logoColor=white" alt="Website"></a>
  <a href="https://github.com/Deep-Learner-msp"><img src="https://img.shields.io/badge/GitHub-Deep--Learner--msp-181717?logo=github&logoColor=white" alt="GitHub"></a>
</p>
