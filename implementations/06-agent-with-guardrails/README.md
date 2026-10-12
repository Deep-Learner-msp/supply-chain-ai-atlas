# 06: An agent with guardrails

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/06-agent-with-guardrails.ipynb)

A delivered load has no proof of delivery, so the invoice is stuck. The agent chases the carrier and closes the case.

```bash
python agent.py
```

```
 1. lookup_shipment  -> {... "pod": null, "invoice": 1850 ...}
 2. issue_credit     -> DENIED by approver: POD is still being chased; no credit yet.
 3. pay_carrier      -> BLOCKED: tool not on the allowed list
 4. email_carrier    -> {"sent_to": "Ravi Transport", ...}
 5. check_inbox      -> {"messages": []}
 6. check_inbox      -> {"messages": [{"from": "Ravi Transport", "attachment": "POD_L-1042.pdf"}]}
 7. attach_pod       -> {"ok": true}
 8. close_case       -> case closed
```

## The four guardrails
1. An **allowed tool list**: anything else is blocked.
2. **Human approval** for anything that moves money.
3. An **audit log** of every step and result.
4. A **step limit**.

The planner is rule-based so it runs offline. Replace it with an LLM that returns `{"tool": ..., "args": ...}`; the guardrail layer stays the same. That separation is the point.

Papers: [Why do multi-agent LLM systems fail?](https://arxiv.org/abs/2503.13657), [Agentic AI autonomy assessment for supply chains](https://arxiv.org/abs/2607.25405), [Reliability of autonomous agents in SCM](https://arxiv.org/abs/2605.17036).
