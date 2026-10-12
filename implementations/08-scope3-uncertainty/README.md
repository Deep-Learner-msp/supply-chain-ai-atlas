# 08: Scope 3 with honest uncertainty, and who to chase first

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/08-scope3-uncertainty.ipynb)

Twelve suppliers, three data sources (primary, modelled, spend-based), a Monte Carlo simulation.

```bash
python uncertainty.py
```

```
Single number most reports show : 5,190 t CO2e
Honest range (90%)              : 3,960 to 7,288 t

Who causes the uncertainty:
  Surfactants    85%   (spend, est. 1300 t)
  Bottles B       9%   (spend, est. 420 t)
  Co-packer       2%   (primary, est. 1500 t)

Get primary data from Surfactants alone and the range narrows from 3,328 t wide to 1,413 t wide.
```

## What to notice
- The biggest supplier (Co-packer) causes 2% of the uncertainty because it already shares primary data.
- One supplier causes 85% of it. That is the first email to send.
- Reporting a range instead of one number is more honest, and it tells you where to spend effort.
