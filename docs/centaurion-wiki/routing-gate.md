# The Routing Gate

The Routing Law made operational. Classifies prediction errors before dispatch.

## Three Dimensions

| Dimension | Range | Low (0) | High (1) |
|-----------|-------|---------|----------|
| **Novelty** | 0-1 | Done many times before | Never encountered |
| **Stakes** | 0-1 | Mistakes are trivial | Mistakes are costly/reputational |
| **Reversibility** | 0-1 | Permanent (sent email, deleted data) | Trivially undone (draft, local edit) |

## Decision Rule

```
IF novelty > 0.7 AND stakes > 0.5 AND reversibility < 0.3:
    → STOP. Surface to human.
ELSE:
    → AI proceeds. Log classification.
```

## Threshold Adjustment

Thresholds are tuned based on outcome data:
- AI tasks getting low ratings → lower thresholds (more conservative)
- Human-surfaced tasks are trivial → raise thresholds (more autonomous)

## Related

- [Three Laws](three-laws.md) — The Routing Law this implements
- [Active Inference Loop](active-inference-loop.md) — Where ROUTE fits in the loop
