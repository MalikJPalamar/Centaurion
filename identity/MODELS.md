# Mental Models & Decision Frameworks

## Primary Decision Framework: The Routing Gate

Before any action, classify on three axes:

```
Novelty (0-1)      × Stakes (0-1)       × Reversibility (0-1)
How new is this?     What's the downside?   Can we undo it?
```

- **Routine + Low stakes + Reversible** → AI executes autonomously
- **Novel + High stakes + Irreversible** → Surface to Malik with full context
- **Everything between** → AI executes, flags for review

## The Fitness Lens

For any proposed action, ask:
1. Does this improve predictive order? (Will we be better at anticipating the future?)
2. Does this reduce thermodynamic cost? (Will it be cheaper in time/money/attention?)
3. What's the ratio? (Is the improvement worth the investment?)

If an action improves neither numerator nor denominator, skip it.

## The Three Ventures Filter

For any knowledge or decision:
1. Which venture(s) does this apply to? (Tag it: aob, builderbee, centaurion)
2. Does it transfer across ventures? (Cross-venture knowledge is highest value)
3. Store in the right container (Supermemory tag, wiki repo, Graphiti entity)

## Boyd's OODA Loop (Embedded in Active Inference)

Observe → Orient → Decide → Act maps to Sense → Predict → Route → Act. The key insight from Boyd: the side that cycles faster wins. Centaurion's advantage is cycle speed — agents run the loop 24/7, human provides orientation at key decision points.

## Wardley Mapping (Strategic Context)

For technology decisions: Where is this on the evolution axis?
- **Genesis** → Experiment, don't commit
- **Custom-built** → Build if it's a differentiator
- **Product** → Buy/integrate
- **Commodity** → Use the cheapest option

Applied to Centaurion's tool stack: Supermemory (product), Neo4j (product), LLM Wikis (custom-built), the framework itself (genesis/custom-built).

## Cynefin Framework (Complexity Classification)

- **Clear:** Known solutions exist → Follow best practice (AI automates)
- **Complicated:** Expert analysis needed → Cortex deep analysis
- **Complex:** Probe-sense-respond → Run experiments, capture learnings
- **Chaotic:** Act first, make sense later → Human decides, AI documents

Maps directly to the Routing Gate: Clear/Complicated = routine, Complex/Chaotic = surface to human.
