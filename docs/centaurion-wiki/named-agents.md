# Named Agents

Centaurion uses three named agents, each with a distinct personality and role. They share state through the [Memory Architecture](memory-architecture.md) and are governed by the [Three Laws](three-laws.md).

## The Agents

### Cortex — The Reasoning Agent

- **Role:** Primary analytical engine. Handles planning, research, code, strategy.
- **Personality:** Precise, structured, transparent about uncertainty. Shows its work.
- **When invoked:** Complex tasks, multi-step reasoning, technical implementation.
- **Defined in:** `agents/Cortex.md`

### Nova — The Creative Agent

- **Role:** Divergent thinking, ideation, content creation, pattern recognition across domains.
- **Personality:** Exploratory, associative, willing to make unexpected connections.
- **When invoked:** Brainstorming, content strategy, reframing problems, creative output.
- **Defined in:** `agents/Nova.md`

### Daemon — The Background Agent

- **Role:** Monitoring, maintenance, automated workflows, health checks.
- **Personality:** Quiet, reliable, surfaces issues only when thresholds are breached.
- **When invoked:** Runs autonomously via scheduled tasks and event triggers.
- **Defined in:** `agents/Daemon.md`

## Routing Between Agents

The [Routing Gate](routing-gate.md) classifies tasks by novelty, stakes, and reversibility. This classification determines which agent handles the task:

| Dimension | Cortex | Nova | Daemon |
|-----------|--------|------|--------|
| High novelty | ✓ | ✓ | |
| High stakes | ✓ | | |
| Low reversibility | → Malik | | |
| Routine monitoring | | | ✓ |
| Creative exploration | | ✓ | |

## Shared State

All agents read from and write to the same state layer:
- **Identity files** (`identity/`) — Who Malik is, what he values
- **Memory layer** — Supermemory, wikis, routing logs
- **Venture tags** — Every action tagged `aob`, `builderbee`, or `centaurion`

This shared state is what makes the agents a system rather than three separate tools.

## Related

- [Three Laws](three-laws.md) — Governance hierarchy for all agents
- [Active Inference Loop](active-inference-loop.md) — The execution loop each agent follows
- [Memory Architecture](memory-architecture.md) — How agents share state
- [11 Levels](11-levels.md) — Named agents represent Level 9 maturity
