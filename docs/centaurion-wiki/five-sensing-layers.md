# The Five Sensing Layers

The Centaurion exo-cortex senses context through five distinct layers, each providing a different resolution of awareness. Together they form the SENSE step of the [Active Inference Loop](active-inference-loop.md).

## The Layers

| Layer | Source | Resolution | Latency |
|-------|--------|-----------|---------|
| **L1 — Identity** | `identity/` files (PURPOSE, MISSION, GOALS, etc.) | Static | Loaded every session |
| **L2 — Memory** | Supermemory, Graphiti temporal graph | Hours–days | Queried per task |
| **L3 — Wiki** | `docs/*-wiki/` compiled knowledge bases | Days–weeks | Read on demand |
| **L4 — Environment** | Git status, file system, running services | Real-time | Polled per action |
| **L5 — External** | Web search, APIs, market data, social signals | Minutes–hours | Fetched when needed |

## Design Principles

- **Layer 1 is always loaded.** Identity is the prior that calibrates everything else.
- **Higher layers are cheaper but staler.** L1–L3 are local files; L4–L5 require runtime access.
- **Sensing is not acting.** The SENSE step gathers; PREDICT interprets. Mixing them causes premature execution.

## How Agents Use Layers

- **Cortex** primarily uses L1–L3 (identity + memory + wiki) for reasoning
- **Nova** specializes in L4–L5 (environment + external) for real-time awareness
- **Daemon** monitors L4 continuously for automated health checks

## Related

- [Active Inference Loop](active-inference-loop.md) — The loop these layers feed into
- [Three Laws](three-laws.md) — The Coupling Law requires all layers stay synchronized
- [Memory Architecture](memory-architecture.md) — How L2 memory is structured
- [Markov Blanket](markov-blanket.md) — The boundary model between layers
