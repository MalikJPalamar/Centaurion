# Claude Hook → Telegram Relay

Phone-readable Claude Code notifications on Linux VPS hosts where Superwhisper.app (macOS-only) cannot run.

## Problem

The official `superwhisper@superwhisper` plugin registers hooks pointing at `/Applications/superwhisper.app/Contents/Resources/claude-hook` — a macOS binary that doesn't exist on a Linux VPS. Without a substitute, Stop / Notification / AskUserQuestion / PermissionRequest fire into a void.

## Solution

The plugin's `hooks.json` invokes its hook command as `${CLAUDE_HOOK:-/Applications/superwhisper.app/...}`. Setting `CLAUDE_HOOK` to a local script reroutes every event through it transparently — no fork of the plugin needed.

We point it at a small bash shim that posts to the same Telegram bot the routing-watchdog already uses (`TELEGRAM_BOT_TOKEN` + `TELEGRAM_HOME_CHANNEL` in `~/.hermes/.env`). One Telegram channel = one place on the phone for all Hermes alerts.

## Install

1. **Shim:** `/root/.claude/bin/claude-hook` (executable). Reads JSON from stdin, branches on `hook_event_name`, posts to Telegram in a backgrounded curl, exits in ~50ms.

2. **Wire it:** add to `~/.claude/settings.json`:
   ```json
   "env": {
     "CLAUDE_HOOK": "/root/.claude/bin/claude-hook"
   }
   ```

3. **Restart Claude Code** — `env` is read at startup, so a running session won't pick it up.

## Behaviour per Event

| Event | Sent | Format |
|---|---|---|
| `Stop` | ✅ | `✅ Claude finished — <project>` |
| `Notification` | ✅ | `🔔 Claude (<project>): <message>` |
| `PreToolUse` (AskUserQuestion only) | ✅ | `❓ Claude asks (<project>): <question>` |
| `PermissionRequest` | ✅ | `🔐 Claude permission (<project>): <reason>` |
| `UserPromptSubmit` | ❌ silent | self-input, no notify |
| Other `PreToolUse` | ❌ silent | log only |

## Design Notes

- **Non-blocking:** curl is forked and disowned. Even a 5s Telegram timeout never stalls Claude Code.
- **Fail-quiet:** missing token, network error → log to `/root/.claude/bin/claude-hook.log`, exit 0. Claude Code keeps moving.
- **Cred source:** lifted from `~/.hermes/.env` at every invocation — rotating the bot token there rotates this hook automatically.
- **Project label:** uses `basename "$cwd"` so Centaurion vs Hermes vs MiroFish are visually distinct in the Telegram thread.

## Verification

```bash
echo '{"hook_event_name":"Stop","cwd":"/root/Centaurion"}' | /root/.claude/bin/claude-hook
tail /root/.claude/bin/claude-hook.log
```

Log should show the dispatch and a Telegram `{"ok":true,...}` reply.

## Porting to Another VPS

1. Copy `/root/.claude/bin/claude-hook` to the target host (or recreate it from this doc).
2. Ensure `~/.hermes/.env` has `TELEGRAM_BOT_TOKEN` and `TELEGRAM_HOME_CHANNEL` — or edit the `ENV_FILE` path at the top of the script.
3. Install the superwhisper plugin: `claude plugin marketplace add superultrainc/superwhisper-claude-code && claude plugin install superwhisper`.
4. Add the `CLAUDE_HOOK` env block to `~/.claude/settings.json`.
5. Restart Claude Code.

## Why Not ntfy / Pushover / Pushbullet

Considered. Telegram won because the bot already exists for the routing-watchdog (`deploy/vps2/routing-watchdog.sh`) — a second channel would fragment phone alerts across two apps. Single-channel ops > multi-channel ops for a phone-first operator.
