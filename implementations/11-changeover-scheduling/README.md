# 11: Changeover scheduling, and why due-date order wastes the shift

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/11-changeover-scheduling.ipynb)

Twelve jobs on one paint line, five colours. Light to dark is a quick clean; dark to light needs a full wash. The changeover depends on the order, so the sequence decides how much of the shift is spent cleaning. Solved with [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver) (`AddCircuit` for the sequence). Synthetic, illustrative data.

```bash
pip install ortools
python changeover.py
```

| Sequence | Total changeover | Makespan | Late jobs | Total tardiness |
|---|---|---|---|---|
| FIFO (arrival order) | 505 min | 1030 min | 9 | 2175 min |
| Due date (EDD) | 430 min | 955 min | 7 | 475 min |
| CP-SAT, least changeover | 65 min | 590 min | 2 | 285 min |
| CP-SAT, fewest late jobs then least changeover | 65 min | 590 min | 1 | 185 min |

## What to notice

- Earliest-due-date order looks responsible but zigzags between colours, so 430 minutes go to cleaning and 7 jobs are still late.
- Grouping light to dark cuts cleaning from 505 to 65 minutes. The freed capacity alone fixes most of the late jobs.
- Adding due dates to the objective costs no extra changeover here and gets late jobs down to 1. Optimise both together, not one after the other.
- Both CP-SAT runs are proven optimal in well under a second. Twelve jobs is small; real lines add more jobs, cleaning crews and shift limits, and the same model shape still holds.
