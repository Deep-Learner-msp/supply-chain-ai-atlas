# 14: Returns disposition, and why "ship it all back" loses money

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/14-returns-disposition.ipynb)

20,000 synthetic returned items in three price bands. Each has a true grade (A restock, B refurbish, C recycle, D scrap) that is uncertain at first touch: we know the return reason and a quick inspection that is right 70% of the time. Synthetic, illustrative prices, costs and probabilities.

```bash
pip install numpy
python disposition.py
```

| Policy | Recovered value | Handling cost | Net | Net per item | Shipped to DC |
|---|---|---|---|---|---|
| Back to DC, then decide | 845,136 | 251,804 | 593,332 | 29.67 | 100% |
| Expected value at first touch | 825,553 | 70,097 | 755,456 | 37.77 | 17% |
| Oracle (true grade known at first touch) | 860,907 | 34,042 | 826,865 | 41.34 | 4% |

Expected value at first touch: combine the return reason (prior) with the inspection result (likelihood) using Bayes' rule, compute the expected net value of each option (restock on the spot, liquidate, recycle, scrap, ship to DC), and pick the highest.

## What to notice

- Deciding at first touch recovers 2% less value, spends 72% less on handling, and nets 162,124 more (+27%).
- The DC still earns its place for uncertain, higher-value items: home goods and electronics that might be restockable or refurbishable get shipped there for proper grading. Accessories never do. The policy ships 17% of items instead of 100%.
- Most of the loss is handling, not grading. An 18-unit accessory that costs 10 to ship and grade is worth less than the trip.
- The gap to the oracle (another 71,409) is the value of a better first-touch inspection. That is where a photo-grading model earns its keep, and you can price it before building it.
