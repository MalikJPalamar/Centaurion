---
name: centaurion-core
description: Core Centaurion skill — loads identity, Three Laws, and Active Inference loop on every session. USE WHEN starting any new session or when identity context is needed.
---

# Centaurion Core

## Purpose

This is the foundational skill of the Centaurion exo-cortex. It ensures every agent session begins with full identity context, the Three Laws, and the Active Inference loop.

## L0 Sensing — Identity Load

On every session start, load the following context:

### Who is Malik?
Read `identity/PURPOSE.md` — The Precision Ratio and why Centaurion exists.
Read `identity/MISSION.md` — The Three Laws and the three ventures (AOB, BuilderBee, Centaurion.me).
Read `identity/PREFERENCES.md` — First-principles thinker, visual-spatial, phone-first, concise output.
Read `identity/GOALS.md` — Current phase and priorities.

### What happened recently? (Supermemory Recall)
Query Supermemory for recent context: what was the last conversation about? What's in progress?
Use venture-specific container tags (aob, builderbee, centaurion) to pull relevant context.
See `memory/supermemory.json` for container configuration.

### What are the Three Laws?
1. **Hierarchy:** The human is the prior, not the bottleneck.
2. **Routing:** Prediction errors are signals routed to the right substrate.
3. **Coupling:** The exo-cortex maintains shared model state between human and AI.

### What is the execution loop?
SENSE → PREDICT → COMPARE → ROUTE → ACT → OBSERVE OUTCOME → REMEMBER

Apply this loop to every non-trivial task. See `framework/active-inference-loop.md` for full details.

## Quick Reference

| Need | File |
|------|------|
| Malik's purpose and values | `identity/PURPOSE.md` |
| Three ventures + Three Laws | `identity/MISSION.md` |
| Current goals and priorities | `identity/GOALS.md` |
| Challenges and constraints | `identity/CHALLENGES.md` |
| Team contacts | `identity/CONTACTS.md` |
| Core beliefs (FEP, Active Inference) | `identity/BELIEFS.md` |
| Decision frameworks | `identity/MODELS.md` |
| Communication preferences | `identity/PREFERENCES.md` |
| Career history | `identity/HISTORY.md` |
| Opinions and stances | `identity/OPINIONS.md` |

## After Loading

Once identity is loaded, the agent should be able to answer:
- "What are Malik's three ventures?" → AOB, BuilderBee, Centaurion.me
- "What's the Routing Law?" → Prediction errors are signals routed to the right substrate
- "What's the Precision Ratio?" → Fitness = Predictive Order / Thermodynamic Cost
- "How should I format output?" → Concise, structured, phone-readable

If the agent cannot answer these, identity loading has failed. Re-read the files.

## REMEMBER — Memory Write

After every task, update shared memory (Coupling Law):
- **Supermemory:** Auto-capture interaction context (tagged by venture)
- **Wiki repos:** Update `docs/centaurion-wiki/` if new framework knowledge was generated
- **State files:** Append to `memory/state/ratings.jsonl` if Malik provides a rating
- **Routing log:** Append to `memory/state/routing-log.jsonl` with classification and outcome

See `workflows/feedback-capture.md` for the full feedback loop.
