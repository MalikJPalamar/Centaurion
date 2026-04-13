# Multi-Runtime Deployment

Centaurion runs across four runtimes, each optimized for a different context and agent personality.

## Architecture

```
VPS1 (primary)          — Daily dev loop, heavy Claude Code execution
Raspberry Pi (edge)     — Ambient local sensing, always-on
OpenClaw (scanner)      — Nova personality, environmental pattern detection
Agent Zero (substrate)  — Autonomous task execution
```

## Runtime Comparison

| Property | VPS1 | Pi | OpenClaw | Agent Zero |
|----------|------|----|----------|------------|
| Agent | Cortex | Cortex (lite) | Nova | Cortex |
| Trigger | Cron (6am CET) | Always-on | Event-driven | Manual / triggered |
| Primary use | Dev loop | Sensing | Scanning | Autonomous tasks |
| Config | `deploy/vps1/` | `deploy/pi/` | `deploy/openclaw/` | `deploy/agent-zero/` |

## Shared State

All runtimes share:
- **Git repo** (`MalikJPalamar/Centaurion`) — source of truth for identity and skills
- **Supermemory** — cross-session, cross-runtime memory store
- **`memory/state/`** — routing log, ratings, and state files (committed to git)

## Deployment Configs

### VPS1
- `settings.json` for Claude Code
- `centaurion-dev-loop.sh` cron script
- Runs `claude -p` with Max subscription

### Pi
- `settings.json` with Centaurion skill paths
- Lightweight skill subset for edge compute

### OpenClaw
- `SOUL.md` personality file (Nova)
- Configured for environmental scanning and signal detection

### Agent Zero
- `system-prompt.md` embedding the Three Laws
- Enables autonomous task routing within bounds

## Related

- [Routing Gate](routing-gate.md) — How tasks get dispatched across runtimes
- [Three Laws](three-laws.md) — Constraints all runtimes operate under
- [Feedback Loop](feedback-loop.md) — How runtime outcomes feed back into the system
