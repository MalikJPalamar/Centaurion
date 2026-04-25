#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Routing Gate Watchdog
# ═══════════════════════════════════════════════════════════
#
# Out-of-band enforcement for the Routing Gate.
# Runs as a SEPARATE process from Hermes. Hermes cannot
# modify, disable, or prevent this from running.
#
# What it does:
#   1. Tails routing-log.jsonl for new tool_call entries
#   2. Validates each classification independently
#   3. Detects: missing classifications, fail-open, drift
#   4. On violation: kills Hermes + alerts Malik
#
# Install:
#   bash deploy/vps2/watchdog-install.sh
#
# Manual run:
#   bash deploy/vps2/routing-watchdog.sh
#
# This is the security camera outside the building.
# ═══════════════════════════════════════════════════════════

set -uo pipefail

CENTAURION_REPO="${CENTAURION_REPO:-$HOME/Centaurion}"
ROUTING_LOG="$CENTAURION_REPO/memory/state/routing-log.jsonl"
WATCHDOG_LOG="$CENTAURION_REPO/logs/watchdog.log"
WATCHDOG_LOCK="$CENTAURION_REPO/logs/.watchdog.lock"
CHECK_INTERVAL="${WATCHDOG_INTERVAL:-30}"
LAST_LINE_FILE="$CENTAURION_REPO/logs/.watchdog-last-line"
ALERT_FILE="$CENTAURION_REPO/memory/state/watchdog-alerts.jsonl"

# ── Thresholds (must match routing_gate.py) ───────────────
NOVELTY_THRESHOLD=0.7
STAKES_THRESHOLD=0.5
REVERSIBILITY_THRESHOLD=0.3

# ── Blocked tool patterns (must match routing_gate.py) ────
BLOCKED_PATTERNS="git push --force|rm -rf|drop database|send_email_to_client|publish|deploy_production"

# ── Telegram alert (optional) ────────────────────────────
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

mkdir -p "$(dirname "$WATCHDOG_LOG")" "$(dirname "$ALERT_FILE")"

# ── Lock ──────────────────────────────────────────────────
if [ -f "$WATCHDOG_LOCK" ]; then
  LOCK_PID=$(cat "$WATCHDOG_LOCK" 2>/dev/null)
  if kill -0 "$LOCK_PID" 2>/dev/null; then
    echo "Watchdog already running (PID $LOCK_PID)"
    exit 0
  fi
  rm -f "$WATCHDOG_LOCK"
fi
echo $$ > "$WATCHDOG_LOCK"
trap 'rm -f "$WATCHDOG_LOCK"' EXIT

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$WATCHDOG_LOG"
}

alert() {
  local severity="$1" message="$2"
  log "🚨 ALERT [$severity]: $message"

  # Write to alerts file
  echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"severity\":\"$severity\",\"message\":\"$message\"}" >> "$ALERT_FILE"

  # Telegram notification (if configured)
  if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d chat_id="$TELEGRAM_CHAT_ID" \
      -d text="🚨 WATCHDOG [$severity]: $message" \
      -d parse_mode="Markdown" \
      >/dev/null 2>&1 || true
  fi
}

kill_hermes() {
  log "⛔ KILLING HERMES — governance violation detected"
  # Kill all Hermes processes
  pkill -f "hermes.*agent" || pkill -f "hermes_cli" 2>/dev/null || true
  # Kill the gateway too
  pkill -f "hermes.*gateway" || true 2>/dev/null || true
  alert "P0" "Hermes killed by watchdog. Routing Gate violation. Manual restart required after investigation."
}

# ── Validation function ──────────────────────────────────
validate_entry() {
  local entry="$1"

  # Parse fields
  local task=$(echo "$entry" | grep -o '"task": *"[^"]*"' | sed 's/.*: *"//;s/"//')
  local novelty=$(echo "$entry" | grep -o '"novelty": *[0-9.]*' | sed 's/.*: *//')
  local stakes=$(echo "$entry" | grep -o '"stakes": *[0-9.]*' | sed 's/.*: *//')
  local reversibility=$(echo "$entry" | grep -o '"reversibility": *[0-9.]*' | sed 's/.*: *//')
  local route=$(echo "$entry" | grep -o '"route": *"[^"]*"' | sed 's/.*: *"//;s/"//')

  # Skip schema lines
  if echo "$entry" | grep -q "_schema"; then
    return 0
  fi

  # Check 1: Blocked patterns should never be ai_autonomous
  if echo "$task" | grep -qiE "$BLOCKED_PATTERNS"; then
    if [ "$route" = "ai_autonomous" ]; then
      alert "P0" "BLOCKED tool passed as autonomous: $task"
      return 1
    fi
  fi

  # Check 2: High novelty + high stakes + low reversibility should be surface_to_human
  if [ -n "$novelty" ] && [ -n "$stakes" ] && [ -n "$reversibility" ]; then
    local should_block=$(echo "$novelty $stakes $reversibility" | awk \
      -v nt="$NOVELTY_THRESHOLD" -v st="$STAKES_THRESHOLD" -v rt="$REVERSIBILITY_THRESHOLD" \
      '{if ($1 > nt && $2 > st && $3 < rt) print "yes"; else print "no"}')

    if [ "$should_block" = "yes" ] && [ "$route" = "ai_autonomous" ]; then
      alert "P1" "High-risk tool classified as autonomous: novelty=$novelty stakes=$stakes reversibility=$reversibility task=$task"
      return 1
    fi
  fi

  # Check 3: Route must be a valid value
  case "$route" in
    ai_autonomous|ai_with_review|surface_to_human) ;;
    *)
      if [ -n "$route" ]; then
        alert "P1" "Invalid route value '$route' for task: $task"
        return 1
      fi
      ;;
  esac

  return 0
}

# ── Heartbeat check ──────────────────────────────────────
check_routing_gate_alive() {
  # If Hermes is running, routing-log should have entries from the last hour
  if pgrep -f "hermes.*agent" || pgrep -f "hermes_cli" >/dev/null 2>&1; then
    if [ -f "$ROUTING_LOG" ]; then
      local last_entry_time=$(tail -1 "$ROUTING_LOG" 2>/dev/null | grep -o '"timestamp": *"[^"]*"' | sed 's/.*: *"//;s/"//')
      if [ -z "$last_entry_time" ]; then
        return 0  # No entries yet, that's ok on startup
      fi
      # Check if Hermes has been running >10 min without any routing log entry
      local hermes_uptime=$(ps -o etimes= -p $(pgrep -f "hermes.*agent" || pgrep -f "hermes_cli" | head -1) 2>/dev/null | tr -d ' ')
      if [ "${hermes_uptime:-0}" -gt 600 ]; then
        # Hermes running >10 min — check log freshness
        local log_age=$(( $(date +%s) - $(stat -c %Y "$ROUTING_LOG" 2>/dev/null || echo "0") ))
        if [ "$log_age" -gt 3600 ]; then
          alert "P2" "Routing log stale (${log_age}s old) while Hermes is running. Gate may be dead."
        fi
      fi
    fi
  fi
}

# ── Main loop ────────────────────────────────────────────
log "═══ Routing Watchdog Starting ═══"
log "Interval: ${CHECK_INTERVAL}s | Log: $ROUTING_LOG"
log "Thresholds: novelty>$NOVELTY_THRESHOLD stakes>$STAKES_THRESHOLD reversibility<$REVERSIBILITY_THRESHOLD"

# Initialize last line tracker
if [ ! -f "$LAST_LINE_FILE" ]; then
  if [ -f "$ROUTING_LOG" ]; then
    wc -l < "$ROUTING_LOG" > "$LAST_LINE_FILE"
  else
    echo "0" > "$LAST_LINE_FILE"
  fi
fi

VIOLATION_COUNT=0

while true; do
  # Check routing gate heartbeat
  check_routing_gate_alive

  # Check for new entries
  if [ -f "$ROUTING_LOG" ]; then
    LAST_LINE=$(cat "$LAST_LINE_FILE" 2>/dev/null || echo "0")
    CURRENT_LINES=$(wc -l < "$ROUTING_LOG")

    if [ "$CURRENT_LINES" -gt "$LAST_LINE" ]; then
      # Process new entries
      NEW_ENTRIES=$(tail -n +"$((LAST_LINE + 1))" "$ROUTING_LOG")

      while IFS= read -r entry; do
        if [ -z "$entry" ]; then continue; fi

        if ! validate_entry "$entry"; then
          VIOLATION_COUNT=$((VIOLATION_COUNT + 1))
          log "Violation #$VIOLATION_COUNT detected"

          # On P0: blocked tool passed as autonomous → kill immediately
          local task_field=$(echo "$entry" | grep -o '"task": *"[^"]*"' | sed 's/.*: *"//;s/"//')
          if echo "$task_field" | grep -qiE "$BLOCKED_PATTERNS" && echo "$entry" | grep -q '"ai_autonomous"'; then
            kill_hermes
          fi

          # On 3 accumulated violations: kill
          if [ "$VIOLATION_COUNT" -ge 3 ]; then
            log "3 violations accumulated — killing Hermes"
            kill_hermes
            VIOLATION_COUNT=0
          fi
        fi
      done <<< "$NEW_ENTRIES"

      echo "$CURRENT_LINES" > "$LAST_LINE_FILE"
    fi
  fi

  sleep "$CHECK_INTERVAL"
done
