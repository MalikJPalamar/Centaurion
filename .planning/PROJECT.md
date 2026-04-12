# PROJECT — Centaurion Exo-Cortex

## Vision

Build a human-AI augmentation framework — an exo-cortex — that Malik Palamar uses daily across three ventures. Grounded in Karl Friston's Free Energy Principle. Maximizes the Precision Ratio: `Fitness = Predictive Order / Thermodynamic Cost`.

## What It Is

A **markdown-native personal AI infrastructure** that:
1. Loads human identity context (TELOS) into every agent session
2. Executes tasks through a 7-step Active Inference loop
3. Routes novel/high-stakes tasks to the human, automates the routine
4. Compounds knowledge across sessions via shared memory
5. Operates across multiple AI runtimes (Claude Code, pi, OpenClaw, Codex)

## What It Is NOT

- Not a web app (existing dashboard is separate)
- Not a TypeScript codebase (no compilation, no Bun, no hooks)
- Not a fork of PAI (cherry-picks patterns, built natively)
- Not an autonomous agent (human is always the prior)

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Content format** | Markdown + JSON | Universal. Any runtime reads it. No build step. |
| **Execution schema** | CLAUDE.md / AGENTS.md | Auto-loaded by Claude Code; readable by any LLM |
| **Skills** | SKILL.md files | Portable across runtimes. Frontmatter + instructions. |
| **Memory (L1)** | Supermemory | Real-time shared bus. Free tier. Plugin ecosystem. |
| **Memory (L2)** | LLM Wiki repos + InfraNodus | Compiled knowledge + topology analysis |
| **Memory (L2b)** | Graphiti + Neo4j | Temporal knowledge graph (Month 2) |
| **Memory (L3)** | MemPalace | Verbatim archive (Month 2) |
| **Sync** | Syncthing | P2P file sync. No git push/pull for live access. |
| **Workflows** | gh-aw + Archon YAML | Scheduled GitHub Actions + workflow DAGs |
| **Testing** | Shell scripts + content validation | Verify file structure, content, and cross-references |

## Constraints

1. **Phone-first.** Malik reviews on phone. No desktop IDE required.
2. **All markdown.** Intelligence lives in prompts, not compiled code.
3. **Budget-conscious.** Free tiers first. Scale only when value proven.
4. **Multi-runtime.** Must work on Claude Code, pi, OpenClaw, Codex.
5. **No secrets in repo.** API keys use REPLACE_WITH_ placeholders.

## Key Stakeholder

**Malik Palamar** — Owner. Reviews from phone. Does not code on desktop. Thinks in systems and metaphors. Runs three ventures: AOB, BuilderBee, Centaurion.me.

## Reference Architecture

**danielmiessler/Personal_AI_Infrastructure (PAI)** — Studied for patterns:
- TELOS identity system (adapted as `identity/`)
- 7-phase Algorithm (adapted as Active Inference loop)
- SKILL.md portable skill format (adopted)
- USER/SYSTEM separation (adopted as identity vs framework)
- Security hooks pattern (adapted as Routing Gate skill)

Not inherited: TypeScript hooks, Bun compilation, flat-file memory, RebuildPAI.ts.
