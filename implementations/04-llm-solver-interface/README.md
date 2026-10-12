# 04: The LLM is the interface, the solver is the engine

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/04-llm-solver-interface.ipynb)

A planner asks what-if questions in plain words. A translator turns each into a structured change, a linear program (OR-Tools) re-optimizes, and the answer explains what moved. The LLM never writes the plan.

```bash
pip install ortools
python whatif.py
```

```
Q: What if the Pune plant shuts for a week?
   Total cost 3,850 -> 6,490 (+2,640).
   Volume changes: Chennai->Mumbai 0->30; Delhi->Mumbai 0->270; Pune->Mumbai 300->0.

Q: What if we hire more drivers?
   Couldn't translate; asking the planner to rephrase.
```

## What to notice

- **The plan is always feasible and optimal** because a solver produced it, not a language model.
- **Unknown questions fail safely.** The translator refuses instead of guessing.
- **Swap in an LLM** by setting `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` (`pip install anthropic`). The rule-based translator is the offline stand-in; nothing else changes.

Papers: [OptiGuide](https://arxiv.org/abs/2307.03875), [LLMs for Supply Chain Decisions](https://arxiv.org/abs/2507.21502), [OptiRepair](https://arxiv.org/abs/2602.19439).
