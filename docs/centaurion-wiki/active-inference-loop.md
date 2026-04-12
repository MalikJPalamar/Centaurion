# The Active Inference Loop

The seven-step execution engine of the Centaurion exo-cortex, grounded in Karl Friston's Free Energy Principle.

## The Loop

```
SENSE → PREDICT → COMPARE → ROUTE → ACT → OBSERVE OUTCOME → REMEMBER
```

## Steps

| Step | What It Does | Failure If Skipped |
|------|-------------|-------------------|
| **SENSE** | Load identity context, recent memory, active alerts | Generic responses ignoring user context |
| **PREDICT** | Form hypothesis with stated confidence | No way to learn from outcomes |
| **COMPARE** | Classify prediction error (routine vs novel) | No routing — agent just acts blindly |
| **ROUTE** | Apply Routing Gate — dispatch to right substrate | Misclassified tasks (false confidence or wasted attention) |
| **ACT** | Execute using skills and tools | — |
| **OBSERVE** | Compare outcome to prediction, assess routing | No learning signal |
| **REMEMBER** | Write to Supermemory, update wikis, log routing | System never improves |

## Key Properties

- **Continuous:** A single task may cycle through the loop multiple times
- **Multi-agent:** Different agents can handle different steps (Nova senses, Cortex reasons)
- **Async-friendly:** Only ROUTE requires synchronous human input (for high-stakes tasks)

## Mapping from PAI

| PAI Algorithm | Centaurion Loop |
|--------------|----------------|
| OBSERVE | SENSE |
| THINK | PREDICT |
| PLAN | COMPARE |
| BUILD | ROUTE |
| EXECUTE | ACT |
| VERIFY | OBSERVE OUTCOME |
| LEARN | REMEMBER |

## Related

- [Fitness Equation](fitness-equation.md) — What the loop optimizes
- [Three Laws](three-laws.md) — Constraints the loop operates under
- [Routing Gate](routing-gate.md) — The ROUTE step in detail
