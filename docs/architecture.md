# Centaurion Architecture

System architecture of the Centaurion exo-cortex.

## Agent Topology

```
┌─────────────────────────────┐
│          Malik (Human)       │
│       The Prior, Not the     │
│          Bottleneck          │
└──────────┬──────────────────┘
           │
    ┌──────▼──────┐
    │   Cortex    │  ← Primary reasoning agent
    │  (Router)   │     Classifies, routes, executes
    └──┬──────┬───┘
       │      │
  ┌────▼──┐ ┌─▼─────┐
  │ Nova  │ │ Daemon │
  │(Voice)│ │(Watch) │
  └───────┘ └────────┘
```

- **Cortex** — The reasoning engine. Runs the Active Inference Loop. Handles task classification, routing, and execution.
- **Nova** — The voice and creative agent. Handles content, communication, and brand expression.
- **Daemon** — The background watcher. Monitors system health, drift detection, and automated workflows.

## Memory Layers

The system uses layered memory for context persistence:

```
┌─────────────────────────────┐
│     Supermemory (Cloud)      │  Long-term cross-session memory
│   Tagged: aob/builderbee/    │  via API
│          centaurion          │
├─────────────────────────────┤
│      Wiki Repos (Local)      │  Structured knowledge bases
│  centaurion-wiki / aob-wiki  │  in markdown
│      / builderbee-wiki       │
├─────────────────────────────┤
│     State Files (Local)      │  Session state, routing logs
│  memory/state/*.jsonl        │  ratings, active context
├─────────────────────────────┤
│    CLAUDE.md (Session)       │  Active instructions loaded
│    identity/ (Session)       │  every conversation start
└─────────────────────────────┘
```

## Decision Flow

Every task passes through the Active Inference Loop:

```
SENSE → PREDICT → COMPARE → ROUTE → ACT → OBSERVE → REMEMBER
```

The **Routing Gate** at step 4 classifies tasks by:
- **Novelty** (0–1): How new is this?
- **Stakes** (0–1): What's the cost of getting it wrong?
- **Reversibility** (0–1): Can we undo it?

High-novelty, high-stakes, low-reversibility tasks surface to Malik. Everything else executes autonomously.

## Venture Structure

Three ventures share the same infrastructure:

| Venture | Wiki | Focus |
|---------|------|-------|
| AOB | `docs/aob-wiki/` | Business education |
| BuilderBee | `docs/builderbee-wiki/` | GHL automation |
| Centaurion | `docs/centaurion-wiki/` | Exo-cortex framework |
