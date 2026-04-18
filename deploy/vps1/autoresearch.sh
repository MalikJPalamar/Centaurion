#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Autoresearch — Autonomous Overnight Iteration
# ═══════════════════════════════════════════════════════════
#
# Reads a research brief from memory/state/autoresearch-active.json,
# runs Claude Code iteratively, and writes results.
#
# Usage:
#   CENTAURION_REPO=~/Centaurion bash deploy/vps1/autoresearch.sh
#
# Schedule for overnight:
#   0 22 * * * cd ~/Centaurion && CENTAURION_REPO=~/Centaurion bash deploy/vps1/autoresearch.sh >> ~/Centaurion/logs/cron.log 2>&1
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$HOME/Centaurion}"
LOG_DIR="$REPO_DIR/logs"
BRIEF="$REPO_DIR/memory/state/autoresearch-active.json"
DATE=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/autoresearch-$DATE.log"
LOCK_FILE="$REPO_DIR/logs/.autoresearch.lock"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ── Lock ──────────────────────────────────────────────────
if [ -f "$LOCK_FILE" ]; then
  LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
  if kill -0 "$LOCK_PID" 2>/dev/null; then
    log "Autoresearch already running (PID $LOCK_PID). Skipping."
    exit 0
  fi
  rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# ── Check for active brief ────────────────────────────────
if [ ! -f "$BRIEF" ]; then
  log "No active research brief at $BRIEF — nothing to research."
  exit 0
fi

log "═══ Autoresearch Starting ═══"

cd "$REPO_DIR"
git pull origin main >> "$LOG_FILE" 2>&1 || true

# Parse brief
QUESTION=$(grep -o '"question": *"[^"]*"' "$BRIEF" | head -1 | sed 's/.*: *"//;s/"//')
VENTURE=$(grep -o '"venture": *"[^"]*"' "$BRIEF" | head -1 | sed 's/.*: *"//;s/"//')
MAX_ITER=$(grep -o '"max_iterations": *[0-9]*' "$BRIEF" | head -1 | sed 's/.*: *//')
MAX_TURNS=$(grep -o '"max_turns_per_iteration": *[0-9]*' "$BRIEF" | head -1 | sed 's/.*: *//')
OUTPUT=$(grep -o '"output": *"[^"]*"' "$BRIEF" | head -1 | sed 's/.*: *"//;s/"//')

MAX_ITER=${MAX_ITER:-3}
MAX_TURNS=${MAX_TURNS:-10}
OUTPUT=${OUTPUT:-"memory/state/autoresearch-results.md"}

log "Question: $QUESTION"
log "Venture: $VENTURE | Iterations: $MAX_ITER | Turns/iter: $MAX_TURNS"
log "Output: $OUTPUT"

# ── Run iterations ────────────────────────────────────────
RESULTS_SO_FAR=""
for i in $(seq 1 "$MAX_ITER"); do
  log "── Iteration $i/$MAX_ITER ──"

  PROMPT="You are Cortex running an autoresearch iteration. Read CLAUDE.md and skills/autoresearch/SKILL.md.

## Research Brief
$(cat "$BRIEF")

## Iteration $i of $MAX_ITER
${RESULTS_SO_FAR:+Previous findings: $RESULTS_SO_FAR}

## Your Task
1. Research the question using available tools (web search if available, file analysis, reasoning)
2. Build on previous findings (don't repeat what's already known)
3. Focus on NEW insights, sources, or connections this iteration
4. Write your findings to $OUTPUT (append, don't overwrite previous iterations)
5. At the end, note what's still unknown for the next iteration
6. Tag: venture=$VENTURE

## Format
Write directly to $OUTPUT. Each iteration adds a section:
### Iteration $i — $(date +%Y-%m-%d)
[findings]
#### Still Unknown
[questions for next iteration]"

  claude -p "$PROMPT" \
    --max-turns "$MAX_TURNS" \
    >> "$LOG_FILE" 2>&1

  log "Iteration $i complete (exit: $?)"

  if [ -f "$REPO_DIR/$OUTPUT" ]; then
    RESULTS_SO_FAR=$(tail -20 "$REPO_DIR/$OUTPUT")
  fi
done

# ── Commit and push ───────────────────────────────────────
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "research($VENTURE): autoresearch — $QUESTION" >> "$LOG_FILE" 2>&1 || true
  git push origin main >> "$LOG_FILE" 2>&1 || log "Push failed"
  log "Results committed and pushed."
fi

# ── Archive the brief ─────────────────────────────────────
ARCHIVE="$REPO_DIR/memory/state/autoresearch-archive-$DATE.json"
mv "$BRIEF" "$ARCHIVE"
log "Brief archived to $ARCHIVE"
log "═══ Autoresearch Complete ═══"
