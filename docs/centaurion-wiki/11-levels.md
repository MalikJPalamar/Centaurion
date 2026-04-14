# The 11 Levels of Agentic Engineering

A maturity model for AI agent systems, from simple prompt-response to fully autonomous exo-cortex. Centaurion uses this framework to assess where each capability sits and what the next evolution looks like.

## The Levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | **Prompt → Response** | Single-turn chat, no memory |
| 2 | **Prompt + Context** | System prompts, few-shot examples |
| 3 | **Tool Use** | Agent calls external tools (search, code execution) |
| 4 | **Multi-Step Chains** | Sequential tool calls with intermediate reasoning |
| 5 | **Branching Agents** | Routing between specialized sub-agents |
| 6 | **Persistent Memory** | Cross-session memory, learning from history |
| 7 | **Self-Monitoring** | Agent evaluates its own outputs, detects errors |
| 8 | **Active Inference** | Agent maintains world model, minimizes prediction error |
| 9 | **Multi-Agent Orchestration** | Named agents collaborate with shared state |
| 10 | **Identity-Aligned Autonomy** | Agent internalizes operator's values, goals, preferences |
| 11 | **Exo-Cortex** | Full cognitive extension — human + AI as unified system |

## Where Centaurion Sits

Centaurion operates primarily at **Levels 8–10**, with the architecture designed for Level 11:

- **Level 8** — The [Active Inference Loop](active-inference-loop.md) drives all task execution through SENSE → PREDICT → COMPARE → ROUTE → ACT → OBSERVE → REMEMBER
- **Level 9** — [Named Agents](named-agents.md) (Cortex, Nova, Daemon) each have distinct roles and share state through the [Memory Architecture](memory-architecture.md)
- **Level 10** — The `identity/` system encodes Malik's purpose, beliefs, models, and preferences so agents align with his values
- **Level 11** — The target: Centaurion as a seamless extension of cognition, governed by the [Three Laws](three-laws.md)

## The Precision Lens

Each level transition should improve the [Precision Ratio](precision-ratio.md): more predictive order per unit of thermodynamic cost. Jumping levels without improving precision creates complexity without value.

## Related

- [Active Inference Loop](active-inference-loop.md) — The core loop (Level 8)
- [Named Agents](named-agents.md) — Multi-agent orchestration (Level 9)
- [Three Laws](three-laws.md) — Governance for autonomous operation
- [Precision Ratio](precision-ratio.md) — How to evaluate level transitions
