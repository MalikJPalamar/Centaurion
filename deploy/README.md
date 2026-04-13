# Centaurion — Deployment Guide

Centaurion runs across four runtimes. Each has its own config in this directory.

## Runtimes

| Runtime | Directory | Purpose | Agent |
|---------|-----------|---------|-------|
| VPS1 | `vps1/` | Daily dev loop, primary Claude Code execution | Cortex |
| Raspberry Pi | `pi/` | Edge sensor / local ambient runtime | Cortex (lite) |
| OpenClaw | `openclaw/` | Environmental scanning and pattern detection | Nova |
| Agent Zero | `agent-zero/` | Autonomous task execution substrate | Cortex |

## VPS1 (Primary)

The main runtime. Runs the daily dev loop via cron.

```bash
# Clone and set up
git clone https://github.com/MalikJPalamar/Centaurion.git ~/centaurion
cd ~/centaurion

# Authenticate Claude
claude auth login

# Install cron (runs at 6am CET daily)
bash deploy/vps1/centaurion-dev-loop.sh --install

# Verify
crontab -l | grep centaurion
```

Logs: `~/centaurion/logs/dev-loop-YYYY-MM-DD.log`

## Raspberry Pi

Edge runtime for ambient sensing and local skill execution.

```bash
# Copy config
cp deploy/pi/settings.json ~/.claude/settings.json

# Run
claude
```

See `pi/settings.json` for skill configuration.

## OpenClaw

Nova personality deployment for environmental scanning.

```bash
# OpenClaw reads SOUL.md on startup
# Place SOUL.md in your OpenClaw personality directory
cp deploy/openclaw/SOUL.md /path/to/openclaw/personalities/nova.md
```

## Agent Zero

Autonomous substrate using Centaurion system prompt.

```bash
# Load system prompt in Agent Zero config
# Reference: deploy/agent-zero/system-prompt.md
```

## Shared Requirements

- Claude Code CLI (`claude`) installed and authenticated
- Git access to `MalikJPalamar/Centaurion`
- `.env` with `SUPERMEMORY_API_KEY` for memory writes

## Updating

All runtimes pull from `main`. VPS1 pulls at the start of each dev loop run. Other runtimes require manual `git pull`.
