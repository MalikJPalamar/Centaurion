# Challenges

## Primary Constraints

### Phone-First Execution
Malik reviews and directs from his phone. He does not code on a desktop. Every interaction must work via:
- **Claude Code app** (Cortex interaction)
- **Termius** (SSH to VPSs)
- **Telegram** (Nova/OpenClaw communication)
- **GitHub mobile** (issue review, PR approval)
- **Obsidian mobile** (wiki browsing)

No nano/vim. No long terminal sessions. No desktop IDE. If it requires a laptop to operate, it's designed wrong.

### JavaScript/TypeScript Beginner
Malik is not a JS/TS developer. The system must not require manual TypeScript compilation, Bun builds, or npm debugging. All intelligence lives in markdown prompts and JSON config — any runtime that reads files can run Centaurion.

### Synoptic Thinker, Not Sequential Executor
Malik thinks in systems, patterns, and metaphors. He sees the whole before the parts. The system should surface connections and patterns, not just execute sequential task lists. Gap analysis, knowledge graphs, and cross-venture synthesis are high-value. Rote task tracking is low-value.

### Three Ventures, One Person
Context-switching between AOB, BuilderBee, and Centaurion is the primary cognitive cost. The memory architecture (Supermemory containers, tagged wikis, Graphiti graph) must make context-switching near-zero: the system remembers what Malik was doing in each venture, so he doesn't have to.

## Secondary Constraints

- **Budget-conscious:** Free tiers first (Supermemory 1M tokens, GitHub Actions). Scale only when value is proven.
- **Two VPSs only:** Hostinger KVM2 instances. No AWS/GCP. Docker for isolation.
- **API key hygiene:** OpenRouter key was exposed in chat. Rotation discipline is critical.
- **Time zone:** Malik operates across European time zones. Agents run 24/7 but human review windows are bounded.
