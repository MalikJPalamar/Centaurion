# Three-Layer Memory Architecture

Centaurion's memory system operates across three layers, each with different persistence, speed, and scope. This mirrors how biological memory works: fast volatile buffers, medium-term working memory, and long-term consolidated storage.

## The Three Layers

### Layer 1: Session Memory (Working Memory)

- **Scope:** Current conversation context
- **Persistence:** Disappears when the session ends
- **Speed:** Instant — it's the active context window
- **Contents:** Current task state, in-progress reasoning, tool results
- **Analogy:** RAM — fast, volatile, limited capacity

### Layer 2: Project Memory (Episodic Memory)

- **Scope:** Cross-session, per-project
- **Persistence:** Stored in `.claude/` memory files and state JSON
- **Speed:** Loaded at session start
- **Contents:** User preferences, feedback history, project context, routing logs
- **Analogy:** SSD — persistent, structured, queryable
- **Files:** `memory/state/routing-log.jsonl`, `memory/state/ratings.jsonl`

### Layer 3: Distributed Memory (Semantic Memory)

- **Scope:** Cross-project, cross-venture
- **Persistence:** External systems (Supermemory, wiki repos, Graphiti)
- **Speed:** Requires API calls or file reads
- **Contents:** Knowledge base, venture wikis, relationship graphs
- **Analogy:** Cloud storage — vast, shared, requires retrieval
- **Locations:** `docs/centaurion-wiki/`, `docs/aob-wiki/`, `docs/builderbee-wiki/`, Supermemory

## How the Layers Interact

The [Active Inference Loop](active-inference-loop.md) REMEMBER step writes to all three layers:

1. **Session:** Updated implicitly as the conversation progresses
2. **Project:** State files updated after each routing decision
3. **Distributed:** Wiki pages and Supermemory updated when new knowledge is generated

The SENSE step reads from all three, prioritizing fresher layers when conflicts arise.

## Memory and the Precision Ratio

Memory quality directly affects the [Precision Ratio](precision-ratio.md):
- **Good memory** = better predictions (higher numerator) at low retrieval cost
- **Bad memory** = stale predictions or expensive searches (worse ratio)

The [Three Laws](three-laws.md) Coupling Law mandates: "Every interaction updates shared memory. The system must compound."

## Related

- [Active Inference Loop](active-inference-loop.md) — The loop that reads/writes memory
- [Named Agents](named-agents.md) — All agents share this memory architecture
- [Three Laws](three-laws.md) — The Coupling Law governs memory updates
- [Precision Ratio](precision-ratio.md) — How memory quality is measured
