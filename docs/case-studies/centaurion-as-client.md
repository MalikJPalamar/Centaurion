# Case Study: Centaurion as Its Own Client

How the Centaurion exo-cortex used its own active inference framework to build itself — and what that proved.

## Context

Centaurion is an AI exo-cortex designed to compound intelligence across Malik's three ventures (AOB, BuilderBee, Centaurion.me). The question: can the system's own methodology (the Three Laws, Active Inference Loop, Precision Ratio) be used to build the system itself?

## Approach

The dev loop applied Centaurion's core framework at every step:

- **Three Laws** governed every decision: Malik remained the prior (Hierarchy), tasks were classified before execution (Routing), and every cycle updated shared memory (Coupling).
- **Active Inference Loop** (SENSE → PREDICT → COMPARE → ROUTE → ACT → OBSERVE → REMEMBER) structured each development iteration.
- **Precision Ratio** (`Predictive Order / Thermodynamic Cost`) determined whether each action was worth taking.

## Method

- TDD-driven development across 8 phases, 288+ automated checks
- Autonomous dev loop running 3x daily on VPS1 (Claude Code, Max subscription)
- Each phase: tests written BEFORE implementation, agent iterates until green
- Routing Gate classified every task — routine → auto-execute, novel/high-stakes → surface to Malik
- GitHub Actions report at 6:15am CET creates Issue for phone review

## Results (as of Phase 7)

| Phase | Tests | Status |
|-------|-------|--------|
| 1: Core Loop | 135/135 | Complete |
| 2: Memory Integration | 15/15 | Complete |
| 3: Multi-Runtime | 13/13 | Complete |
| 4: Knowledge Depth | 33/33 | Complete |
| 5: Operational Workflows | 27/27 | Complete |
| 6: Cross-Venture Coherence | 26/26 | Complete |
| 7: Production Deployment | 9/16 | In progress — blocked on VPS access + API keys |
| **Total** | **280/288** | 97% |

### Timeline

- Day 1: Phase 0-1 built manually (identity, framework, CLAUDE.md, tests)
- Day 2: Phase 2-3 completed by dev loop (memory, deploy configs)
- Day 3: Phase 4-6 cleared in 12 hours after increasing cadence to 3x daily
- Day 4+: Phase 7 hitting real deployment blockers (NanoClaw, Supermemory)

### Key Observations

1. **Content scales fast, deployment scales slow.** The agent created 60+ files of framework content in days. Connecting to real systems (NanoClaw, Supermemory) requires human VPS access.
2. **TDD works for markdown systems.** Writing structural tests (file exists, contains keywords, cross-references resolve) before implementation prevents hollow content.
3. **The Routing Law proved itself.** Phase 7 tests naturally separated into "agent can fix" vs "needs Malik" — exactly the routing pattern the framework describes.
4. **3x daily cadence was the unlock.** At 1x daily (3 fixes), backlog estimated 18 days. At 3x daily (10 fixes, 30 turns), cleared in 12 hours.

## What It Proves

Centaurion's methodology works for building Centaurion. The Active Inference loop drives iterative improvement, the Routing Gate correctly separates human vs. AI work, and the Coupling Law (shared state via git + test suite) keeps the system coherent across sessions.

The limitation: the framework excels at knowledge architecture and content coherence. Production deployment still requires human access to infrastructure. The centaur pattern holds — neither half alone reaches the peak.
