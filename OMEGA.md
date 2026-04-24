# OMEGA — Centaurion Rebuilt

> Codename: Omega
> What: Centaurion's identity + framework + routing, running on Hermes + browser-harness + Pi infrastructure
> Why: Self-improving agent with principled decision architecture. No one else has this combination.

## The Stack

```
┌─────────────────────────────────────────────────────────┐
│                    CENTAURION LAYER                       │
│  Three Laws · Precision Ratio · Active Inference Loop    │
│  TELOS Identity · Routing Gate · Cross-Venture Context   │
│  This is what makes Omega different from every other     │
│  agent — principled governance, not ad-hoc prompting.    │
├─────────────────────────────────────────────────────────┤
│                    OMEGA BRIDGE                           │
│  omega/extensions/centaurion-core.py  — Identity loader  │
│  omega/extensions/routing-gate.py     — Classification   │
│  omega/extensions/memory-bridge.py    — Supermemory sync │
│  omega/extensions/venture-tagger.py   — AOB/BB/C tagging │
│  omega/skills/                        — Centaurion skills │
│  omega/SOUL.md                        — Cortex for Hermes│
├─────────────────────────────────────────────────────────┤
│                    HERMES ENGINE                          │
│  Self-improving skills · SQLite persistent memory        │
│  Multi-platform gateway (Telegram/Discord/Slack/Email)   │
│  MCP native · 40+ tools · Cron scheduler                 │
│  Parent-child delegation · Fallback providers            │
│  Honcho dialectic reasoning (optional)                   │
├─────────────────────────────────────────────────────────┤
│                    BROWSER-HARNESS                        │
│  Self-healing CDP automation · 80+ domain skills         │
│  Agent-editable helpers · Registered as Hermes tool      │
├─────────────────────────────────────────────────────────┤
│                    PI INFRASTRUCTURE                      │
│  Multi-provider LLM API · Session branching              │
│  Extension system · agentskills.io standard              │
│  Model catalog (300+) · RPC integration                  │
└─────────────────────────────────────────────────────────┘
```

## What Each Layer Contributes

### Centaurion (the brain — KEPT)
- `identity/` → Becomes Hermes SOUL.md + MEMORY.md
- `framework/` → Becomes Hermes skills (agentskills.io format)
- `agents/Cortex.md` → Becomes the master SOUL.md
- `skills/routing-gate/` → Becomes a Hermes extension (tool_call interceptor)
- `CLAUDE.md` → Stays for Claude Code sessions (coexists)
- Three Laws enforcement at every decision point
- TDD test suite (keeps running, extended for Omega)

### Hermes (the engine — INTEGRATED)
- Agent loop: synchronous orchestration with tool dispatch
- Memory: SQLite sessions + MEMORY.md + USER.md + Honcho
- Gateway: Telegram, Discord, Slack, WhatsApp, Signal, Email
- Skills: self-creating, self-improving during use
- Cron: natural language scheduling (replaces bash cron)
- MCP: native client + server
- Delegation: parent-child agent spawning

### Browser-Harness (the hands — TOOL)
- Registered as a Hermes tool via helpers integration
- Self-healing: edits own helpers.py when encountering new patterns
- 80+ domain skills (GitHub, LinkedIn, Amazon, etc.)
- Centaurion-specific browser skill for venture monitoring

### Pi (the foundation — REFERENCE)
- agentskills.io standard (skills format shared with Hermes + Claude Code)
- Extension architecture patterns (event hooks, tool interception)
- Session branching model (non-linear reasoning)
- Multi-provider LLM abstraction

## Directory Structure

```
centaurion/                          # Existing repo
├── CLAUDE.md                        # Claude Code schema (kept)
├── OMEGA.md                         # This file
├── identity/                        # TELOS (kept, source of truth)
├── framework/                       # Theoretical core (kept)
├── agents/                          # Personalities (kept)
├── skills/                          # Centaurion skills (kept, deployed to Hermes)
├── memory/                          # Config pointers (kept)
├── docs/                            # Wikis (kept)
│
├── omega/                           # NEW — The integration layer
│   ├── SOUL.md                      # Cortex personality for Hermes
│   ├── MEMORY.md                    # Persistent facts for Hermes
│   ├── USER.md                      # Malik profile for Hermes
│   ├── config.yaml                  # Hermes config with Omega extensions
│   │
│   ├── extensions/                  # Hermes extensions (Python)
│   │   ├── centaurion_core.py       # Loads identity on session_start
│   │   ├── routing_gate.py          # Intercepts tool_calls, classifies
│   │   ├── memory_bridge.py         # Syncs Supermemory ↔ Hermes memory
│   │   ├── venture_tagger.py        # Auto-tags interactions by venture
│   │   └── dev_loop.py              # TDD dev loop as Hermes cron task
│   │
│   ├── skills/                      # Hermes-format skills
│   │   ├── centaurion-core/SKILL.md
│   │   ├── routing-gate/SKILL.md
│   │   ├── browser-automation/SKILL.md
│   │   └── autoresearch/SKILL.md
│   │
│   ├── tools/                       # Custom Hermes tools
│   │   ├── browser_harness.py       # Registers browser-harness as tool
│   │   └── wiki_manager.py          # CRUD for venture wikis
│   │
│   └── install.sh                   # One-command Omega setup
│
├── deploy/                          # Deployment configs (kept + extended)
│   ├── vps1/                        # VPS1: dev loop, NanoClaw
│   ├── vps2/                        # NEW: Hermes + browser-harness
│   ├── hermes/                      # Hermes config
│   └── browser-harness/             # Browser setup
│
└── tests/                           # TDD suite (extended for Omega)
    ├── verify-core-loop.sh          # Phase 1 (kept)
    ├── ...                          # Phases 2-10 (kept)
    └── verify-omega.sh              # Phase 11: Omega integration
```

## Implementation Plan

### Sprint 1: The Bridge (This Session)
1. Create `omega/` directory structure
2. Build `omega/SOUL.md` — Cortex for Hermes (enhanced from deploy/hermes/)
3. Build `omega/extensions/centaurion_core.py` — loads identity on session_start
4. Build `omega/extensions/routing_gate.py` — intercepts tool calls
5. Build `omega/tools/browser_harness.py` — registers browser as Hermes tool
6. Write Phase 11 TDD tests
7. Push to omega/rebuild branch

### Sprint 2: Engine Integration (Next Session)
1. Deploy to VPS2: install Omega extensions in Hermes
2. Test: `hermes` → responds as Cortex with Three Laws
3. Test: Routing Gate intercepting tool calls
4. Test: browser-harness accessible as a tool
5. Migrate dev loop from bash cron to Hermes cron

### Sprint 3: Gateway & Memory (Week 2)
1. Enable Telegram gateway → replaces NanoClaw for Nova
2. Connect Supermemory via memory_bridge extension
3. Connect Honcho for dialectic reasoning
4. Test cross-platform: Telegram → Hermes → Cortex response

### Sprint 4: Self-Improvement (Week 2-3)
1. Enable Hermes skill auto-creation from Centaurion tasks
2. Route new skills through Routing Gate validation
3. Enable skill improvement during use
4. First autoresearch run through Hermes (not bash script)

## What Makes Omega Different

Every other agent framework is either:
- **Powerful but unprincipled** (Hermes, AutoGPT) — acts without governance
- **Principled but static** (Centaurion today) — governs but doesn't self-improve
- **Capable but narrow** (browser-harness) — does one thing well

Omega is the first system that combines:
1. **Principled governance** (Three Laws, Routing Gate, Precision Ratio)
2. **Self-improving execution** (Hermes skill creation + improvement)
3. **Persistent identity** (TELOS across all sessions and platforms)
4. **Web autonomy** (browser-harness self-healing automation)
5. **Multi-platform presence** (Telegram, Discord, Slack, Email, CLI)
6. **Cross-venture context** (AOB, BuilderBee, Centaurion.me tagged memory)

The centaur doesn't just think well. It thinks well, acts autonomously within principled bounds, remembers everything, improves from experience, and operates everywhere.
