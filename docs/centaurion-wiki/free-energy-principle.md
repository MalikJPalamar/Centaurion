# Free Energy Principle

Karl Friston's Free Energy Principle (FEP) states that all persistent systems minimize variational free energy — the difference between their model of the world and the actual sensory data they receive. This is the theoretical foundation of the Centaurion exo-cortex.

## Core Idea

A system that persists must either:
1. **Update its model** to better predict incoming data (perceptual inference)
2. **Act on the world** to make data match its predictions (active inference)

Both strategies reduce surprise. The Centaurion system does both:
- SENSE → PREDICT → COMPARE updates the model (strategy 1)
- ROUTE → ACT changes the world (strategy 2)

## From Theory to Practice

| FEP Concept | Centaurion Implementation |
|------------|--------------------------|
| Variational free energy | Prediction error in the [Active Inference Loop](active-inference-loop.md) |
| Precision weighting | The [Precision Ratio](precision-ratio.md) |
| Markov blanket | The [Markov Blanket](markov-blanket.md) boundary model |
| Generative model | Identity files + wiki + memory layers |
| Active inference | The [Routing Gate](routing-gate.md) dispatching actions |

## Why This Framework

Most AI assistant systems are reactive — they wait for instructions. The FEP framing makes Centaurion **proactive**: it maintains predictions about what Malik needs and acts to reduce surprise. The [Three Laws](three-laws.md) constrain this proactivity so the AI augments rather than overrides.

## Related

- [Active Inference Loop](active-inference-loop.md) — FEP made operational
- [Precision Ratio](precision-ratio.md) — The optimization metric derived from FEP
- [Markov Blanket](markov-blanket.md) — The boundary model from FEP
