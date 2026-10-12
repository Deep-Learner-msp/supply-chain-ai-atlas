# 07. Return: reverse logistics

## Decisions
Restock, refurbish, resell, recycle or scrap. Where to send it.

## What fits
| Sub-problem | Type | Reach for |
|---|---|---|
| Disposition | Prediction + planning | Condition classification feeding a value-maximizing decision |
| Return reason extraction | Documents | LLM on free-text reasons |
| Network design for returns | Planning | Facility location optimization |

## Open problems
- Returns are rarely forecast at all, so reverse capacity is planned last.
- Grading condition from photos consistently enough to automate.
