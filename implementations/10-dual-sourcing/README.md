# 10: Dual sourcing, and why it loses on average and wins when it counts

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/10-dual-sourcing.ipynb)

A brand needs 1,000 units a week. The far supplier costs 10.00 a unit but can be shut down for 4 to 16 weeks by a disruption. The near supplier costs 12.50 and is rarely disrupted. A lost sale costs 25. We simulate 20,000 years. Synthetic, illustrative numbers.

```bash
pip install numpy
python dual_sourcing.py
```

| Policy | Mean annual cost | P95 year | P99 year | Worst year |
|---|---|---|---|---|
| Single far | 547,772 | 715,000 | 775,000 | 1,060,000 |
| Single near | 656,045 | 687,500 | 825,000 | 1,037,500 |
| Dual 80/20 (near can surge to 60%) | 568,576 | 645,320 | 680,320 | 820,320 |

The far supplier is disrupted at some point in 19% of simulated years, the near one in 5%.

## What to notice

- Dual sourcing costs 20,804 more in an average year (+3.8%). On a spreadsheet of expected cost, it loses every time.
- In a 1-in-20 bad year it costs 69,680 less (-9.7%), and the worst year is about 240,000 cheaper. That is what the premium buys.
- Single near is the most expensive on average and still not the safest: one supplier is one point of failure, however close it is.
- The surge clause (reserved near capacity, paid for every week) is what makes the second source useful in a crisis. A second supplier with no spare capacity is not much of a hedge.
- Report sourcing decisions with a tail metric (P95 or P99 cost) next to the mean, or the cheap single source always wins the meeting.
