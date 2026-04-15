# Getting Started with Centaurion

How to set up and run the Centaurion exo-cortex in a new session.

## Prerequisites

- Git
- Claude Code CLI (or compatible agent runner)
- Access to this repository

## Setup

1. **Clone the repo**
   ```bash
   git clone <repo-url> && cd Centaurion
   ```

2. **Read CLAUDE.md** — this is the system's entry point. It defines the Three Laws, the Active Inference Loop, and all routing behavior.

3. **Load identity** — the agent reads `identity/PURPOSE.md`, `identity/MISSION.md`, `identity/GOALS.md`, and `identity/PREFERENCES.md` on every session start.

4. **Verify the install** — run the test suite:
   ```bash
   bash tests/run-all.sh
   ```

## Key Directories

| Directory | What's Inside |
|-----------|--------------|
| `identity/` | Malik's TELOS identity system |
| `agents/` | Cortex, Nova, Daemon personalities |
| `skills/` | Portable SKILL.md files |
| `framework/` | Three Laws, Precision Ratio, routing gate |
| `memory/` | Supermemory config, wiki pointers, state |
| `workflows/` | Automated health checks and feedback capture |
| `docs/` | Wikis (AOB, BuilderBee, Centaurion), architecture |

## First Session Checklist

- [ ] Agent reads CLAUDE.md and loads identity
- [ ] Confirm the Three Laws are active (Hierarchy, Routing, Coupling)
- [ ] Check memory state in `memory/state/`
- [ ] Run a test task through the Active Inference Loop
