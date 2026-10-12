# 05: Dock scheduling, and why stable re-plans beat optimal ones

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/05-dock-scheduling.ipynb)

Ten trucks, three dock doors, OR-Tools CP-SAT. Then one truck runs 50 minutes late.

```bash
pip install ortools
python docks.py
```

| Plan | Total wait | Trucks moved |
|---|---|---|
| Original | 95 min | |
| Free re-plan (best total wait) | 75 min | 7 |
| Stable re-plan (penalty for moving trucks) | 120 min | 1 |

## What to notice

- The optimal re-plan saves 20 minutes by moving seven trucks. Seven drivers get new doors and times; the yard team rebuilds its plan.
- The stable re-plan moves only the late truck. It costs 45 more minutes of waiting, and the floor can actually follow it.
- Real schedulers need both terms in the objective. "Optimal" without stability is a schedule nobody trusts.
