# Centaurion — Deployment Guide

Centaurion runs across multiple runtimes. Each has its own config in this directory.

## Runtimes

| Runtime | Directory | VPS | Agent | Status |
|---------|-----------|-----|-------|--------|
| Claude Code | `vps1/` | VPS1 (148.230.117.105) | Cortex | Running (3x daily cron) |
| NanoClaw | `nanoclaw/` | VPS1 | Nova | Running (Docker, Telegram) |
| Pi coding-agent | `pi/` | VPS1 | Cortex (lite) | Config ready |
| Agent Zero | `agent-zero/` | VPS2 | Cortex | Config ready |

## VPS1 — One-Command Setup

```bash
# From scratch:
curl -sL https://raw.githubusercontent.com/MalikJPalamar/Centaurion/main/install.sh | bash

# Or if repo is already cloned:
cd ~/Centaurion && bash install.sh
```

The installer handles: clone/pull, auth check, cron install (dev loop 3x daily + weekly review + health check), NanoClaw SOUL.md deploy, and test suite.

## VPS1 — Manual Setup

```bash
git clone https://github.com/MalikJPalamar/Centaurion.git ~/Centaurion
cd ~/Centaurion
claude auth login                    # Authenticate with Max subscription

# Install all cron jobs
CENTAURION_REPO=~/Centaurion bash deploy/vps1/centaurion-dev-loop.sh --install

# Deploy Nova to NanoClaw
cp agents/Nova.md ~/nanoclaw/SOUL.md

# Verify
CENTAURION_REPO=~/Centaurion bash deploy/vps1/health-check.sh
```

### Cron Schedule (VPS1)

| Job | UTC | CET | Script |
|-----|-----|-----|--------|
| Health check | 03:55 | 05:55 | `deploy/vps1/health-check.sh` |
| Dev loop (morning) | 04:00 | 06:00 | `deploy/vps1/centaurion-dev-loop.sh` |
| Dev loop (afternoon) | 12:00 | 14:00 | `deploy/vps1/centaurion-dev-loop.sh` |
| Dev loop (evening) | 20:00 | 22:00 | `deploy/vps1/centaurion-dev-loop.sh` |
| Weekly review | 05:00 Mon | 07:00 Mon | `deploy/vps1/weekly-review.sh` |

### Logs

```
~/Centaurion/logs/
├── dev-loop-YYYY-MM-DD.log    # Dev loop execution log (rotated 14 days)
├── weekly-review-YYYY-MM-DD.log
├── cron.log                    # Cron stdout/stderr
```

### Status Files

```
memory/state/
├── dev-loop-status.json        # Last dev loop result
├── health-status.json          # Last health check
├── weekly-review-YYYYWNN.md    # Weekly review outputs
├── ratings.jsonl               # Outcome ratings
├── routing-log.jsonl           # Routing Gate classifications
```

## NanoClaw — Nova Personality

Nova runs on NanoClaw (Docker) on VPS1, connected via Telegram.

```bash
# Deploy personality
cp ~/Centaurion/agents/Nova.md ~/nanoclaw/SOUL.md

# Verify container is running
docker ps | grep -i claw

# Check model config (should use free model)
grep MODEL ~/nanoclaw/.env
```

## Pi Coding-Agent

```bash
mkdir -p ~/.pi/agent/skills/centaurion
cp deploy/pi/settings.json ~/.pi/agent/settings.json
cp skills/centaurion-core/SKILL.md ~/.pi/agent/skills/centaurion/
```

## Agent Zero (VPS2)

Copy the system prompt into Agent Zero's config:

```bash
cp deploy/agent-zero/system-prompt.md /path/to/agent-zero/prompts/default/agent.system.md
```

## GitHub Actions (Report Only)

The `.github/workflows/daily-dev-loop.yml` runs at 6:15am CET and creates a GitHub Issue with test results. No Claude Code, no API cost — pure shell + GitHub API.
