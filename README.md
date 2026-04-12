# Centaurion

> A human-AI augmentation framework grounded in the Free Energy Principle.

## What Is Centaurion?

Centaurion is an **exo-cortex** — a composite human-AI system that maximizes the Precision Ratio:

```
Precision = Predictive Order / Thermodynamic Cost
```

The human (Malik Palamar) provides calibration: values, taste, strategic direction. The AI agents (Cortex, Nova, Daemon) provide execution: analysis, memory, tireless iteration. Neither reaches the fitness peak alone. Together, they form a centaur.

## The Three Laws

1. **Hierarchy Law:** The human is the prior, not the bottleneck.
2. **Routing Law:** Prediction errors are signals routed to the right substrate.
3. **Coupling Law:** The exo-cortex maintains shared model state between human and AI.

## Architecture

### Exo-Cortex Infrastructure

```
identity/       Who Malik is — TELOS identity system (10 files)
framework/      How we think — Three Laws, Precision Ratio, Active Inference loop
agents/         Who we are — Cortex (reasoning), Nova (sensing), Daemon (identity root)
skills/         What we can do — portable SKILL.md files for any runtime
memory/         Where we remember — Supermemory, LLM Wikis, Graphiti, MemPalace
workflows/      What runs automatically — daily health, weekly gap analysis
```

### Web Dashboard (existing)

```
frontend/       React + TypeScript dashboard UI
backend/        FastAPI backend with API endpoints
Cognitive-Company/  Business operations structure
```

### Named Agents

| Agent | Role | Runtime | Metaphor |
|-------|------|---------|----------|
| **Cortex** | Reasoning, deep analysis, strategic planning | Claude Code | Prefrontal cortex |
| **Nova** | Environmental scanning, signal detection | OpenClaw + Telegram | Afferent nervous system |
| **Daemon** | Identity root, personal API, MCP server | Daemon project | The Greek daimon |

### Three Ventures

| Venture | Malik's Role | Primary Agent |
|---------|-------------|---------------|
| **AOB** | Head of IT & Applied Intelligence | Nova |
| **BuilderBee** | Fractional CEO | Cortex |
| **Centaurion.me** | Founder | Cortex |

## Quick Start

### For Claude Code
Open this repo in Claude Code. `CLAUDE.md` loads automatically, configuring the agent as Cortex with the Active Inference loop.

### For Other Runtimes
Read `AGENTS.md` for pi, OpenClaw, Codex, or Agent Zero configuration.

### Key Entry Points
- `CLAUDE.md` — Execution schema (Claude Code)
- `AGENTS.md` — Multi-runtime schema
- `identity/PURPOSE.md` — Why Centaurion exists
- `identity/MISSION.md` — Three Laws + three ventures
- `framework/active-inference-loop.md` — The seven-step execution loop
- `skills/centaurion-core/SKILL.md` — Core skill (loads identity + loop)

## Memory Architecture

```
Layer 1: Supermemory     — Real-time shared bus (ambient capture + recall)
Layer 2: LLM Wikis      — Compiled knowledge (three venture-specific repos)
         InfraNodus      — Knowledge topology (gap analysis, clusters)
         Graphiti/Neo4j  — Temporal graph (how facts change over time)
Layer 3: MemPalace       — Verbatim archive (raw conversation exports)
```

## Design Principles

- **All markdown, no TypeScript hooks.** The intelligence lives in the prompts. Any runtime that reads markdown can run Centaurion.
- **Phone-first.** Everything works from Termius, Claude app, Telegram, or GitHub mobile.
- **Memory compounds.** Every interaction leaves the system smarter.
- **Patterns from PAI, not code from PAI.** Cherry-picked from danielmiessler/Personal_AI_Infrastructure: TELOS identity, Algorithm structure, skill architecture. Built natively.

## License

MIT
