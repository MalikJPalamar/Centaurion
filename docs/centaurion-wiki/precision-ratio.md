# The Precision Ratio

```
Precision = Predictive Order / Thermodynamic Cost = -ε / C
```

## What It Means

Every persistent system is a prediction machine. Precision — in Active Inference terms — is the confidence-weight on predictions. The Precision Ratio measures how sharply a system models reality relative to the cost of maintaining those models.

## Components

**Predictive Order (numerator):** The system's accuracy in anticipating what the user needs, what clients want, what the market will do. Measured by routing accuracy, recommendation acceptance, and Malik's outcome ratings.

**Thermodynamic Cost (denominator):** Time, money, cognitive load, and compute consumed. Measured by time-to-completion, monthly API spend, and context-switch frequency.

## Application in Centaurion

Every design decision is evaluated through this lens:
- Does this improve predictive order? → Will we anticipate better?
- Does this reduce thermodynamic cost? → Will it be cheaper to operate?
- If neither → question whether it's worth doing.

## Related

- [Three Laws](three-laws.md) — The governing constraints
- [Active Inference Loop](active-inference-loop.md) — The execution engine
- [Routing Gate](routing-gate.md) — How prediction errors are classified
