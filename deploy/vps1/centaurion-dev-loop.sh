#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Daily Development Loop — VPS1 Cron Script
# ═══════════════════════════════════════════════════════════
#
# Runs Claude Code against failing tests using Max subscription.
# Scheduled via cron (3x daily) on VPS1.
#
# Install:
#   CENTAURION_REPO=~/Centaurion bash deploy/vps1/centaurion-dev-loop.sh --install
#
# Manual run:
#   CENTAURION_REPO=~/Centaurion bash deploy/vps1/centaurion-dev-loop.sh
#
# Logs: ~/Centaurion/logs/dev-loop-YYYY-MM-DD.log
# Status: memory/state/dev-loop-status.json
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$HOME/Centaurion}"
LOG_DIR="$REPO_DIR/logs"
LOCK_FILE="$REPO_DIR/logs/.dev-loop.lock"
STATUS_FILE="$REPO_DIR/memory/state/dev-loop-status.json"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LOG_FILE="$LOG_DIR/dev-loop-$DATE.log"
MAX_TURNS=30
MAX_FIXES=10
START_TIME=$(date +%s)

# ── Install mode ──────────────────────────────────────────
if [ "${1:-}" = "--install" ]; then
  mkdir -p "$LOG_DIR"
  CRON_BASE="cd $REPO_DIR && CENTAURION_REPO=$REPO_DIR bash deploy/vps1/centaurion-dev-loop.sh >> $LOG_DIR/cron.log 2>&1"

  if crontab -l 2>/dev/null | grep -q "centaurion-dev-loop"; then
    echo "Cron jobs already installed:"
    crontab -l | grep "centaurion-dev-loop"
  else
    (crontab -l 2>/dev/null
     echo "0 4 * * * $CRON_BASE"
     echo "0 12 * * * $CRON_BASE"
     echo "0 20 * * * $CRON_BASE"
    ) | crontab -
    echo "Cron jobs installed (3x daily: 6am, 2pm, 10pm CET):"
    crontab -l | grep "centaurion-dev-loop"
  fi
  exit 0
fi

# ── Uninstall mode ────────────────────────────────────────
if [ "${1:-}" = "--uninstall" ]; then
  crontab -l 2>/dev/null | grep -v "centaurion-dev-loop" | crontab -
  rm -f "$LOCK_FILE"
  echo "Cron jobs removed."
  exit 0
fi

# ── Concurrency lock ──────────────────────────────────────
mkdir -p "$LOG_DIR"

if [ -f "$LOCK_FILE" ]; then
  LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
  if kill -0 "$LOCK_PID" 2>/dev/null; then
    echo "[$(date '+%H:%M:%S')] Dev loop already running (PID $LOCK_PID). Skipping." | tee -a "$LOG_FILE"
    exit 0
  else
    rm -f "$LOCK_FILE"
  fi
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# ── Helpers ───────────────────────────────────────────────
log() {
  echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

write_status() {
  local status="$1" phase="${2:-0}" fixed="${3:-0}" remaining="${4:-0}" elapsed="${5:-0}"
  cat > "$STATUS_FILE" <<STATUS_JSON
{
  "timestamp": "$TIMESTAMP",
  "date": "$DATE",
  "status": "$status",
  "phase": $phase,
  "tests_fixed": $fixed,
  "tests_remaining": $remaining,
  "elapsed_seconds": $elapsed,
  "max_turns": $MAX_TURNS,
  "max_fixes": $MAX_FIXES
}
STATUS_JSON
}

# ── Log rotation (keep last 14 days) ──────────────────────
find "$LOG_DIR" -name "dev-loop-*.log" -mtime +14 -delete 2>/dev/null || true

# ── Main execution ────────────────────────────────────────
log "═══ Centaurion Dev Loop Starting ═══"
log "Date: $DATE | Max turns: $MAX_TURNS | Max fixes: $MAX_FIXES"
log "Repo: $REPO_DIR"

# Step 1: Pull latest
log "Pulling latest from main..."
cd "$REPO_DIR"
git pull origin main >> "$LOG_FILE" 2>&1 || {
  log "ERROR: git pull failed"
  write_status "error" 0 0 0 $(($(date +%s) - START_TIME))
  exit 1
}

# Step 2: Run tests and identify priority
log "Running test suite..."
PRIORITY_JSON=$(bash tests/identify-next-priority.sh 2>/dev/null)
STATUS=$(echo "$PRIORITY_JSON" | grep -o '"status": *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')
PHASE=$(echo "$PRIORITY_JSON" | grep -o '"phase": *[0-9]*' | head -1 | sed 's/.*: *//')
FIRST_FAIL=$(echo "$PRIORITY_JSON" | grep -o '"first_failure": *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')
TOTAL_FAIL=$(echo "$PRIORITY_JSON" | grep -o '"fail": *[0-9]*' | tail -1 | sed 's/.*: *//')
TOTAL_FAIL=${TOTAL_FAIL:-0}

log "Status: $STATUS | Phase: $PHASE | Failures: $TOTAL_FAIL"

if [ "$STATUS" = "all_passing" ]; then
  log "All tests passing. Nothing to develop."
  write_status "all_passing" "$PHASE" 0 0 $(($(date +%s) - START_TIME))
  log "═══ Dev Loop Complete (no work needed) ═══"
  exit 0
fi

log "First failure: $FIRST_FAIL"

# Step 3: Run Claude Code to fix failing tests
log "Running Claude Code (Max subscription)..."

PROMPT="You are Cortex, the Centaurion daily development loop. Read CLAUDE.md for your identity and the Active Inference loop.

## Current State
$(echo "$PRIORITY_JSON")

## Your Task
Fix the failing tests by building REAL implementation — runnable scripts, accurate content, operational configs. NOT placeholder content that just matches grep patterns.

### Rules
1. Read the failing test to understand EXACTLY what it checks
2. Read related source files to understand context and patterns
3. Build the REAL implementation:
   - Scripts must be runnable (bash -n passes, real commands)
   - Wiki content must be factually accurate (AOB = Art of Breath, not Brilliance)
   - Config files must have real structure (valid JSON/YAML)
   - Cross-references must resolve to actual files
4. Run the phase test to verify your fix
5. Run \`bash tests/run-all.sh\` to check for regressions
6. Stage and commit passing changes
7. Fix up to $MAX_FIXES tests per run
8. If a test requires VPS-specific access (SSH, Docker, external APIs) that you cannot provide, SKIP it and move to the next

### Quality Standards
- Prefer operational code over documentation
- Every script must be executable and do real work
- Wiki pages must contain specific, accurate information — not generic templates
- Cross-venture connections must reference real shared patterns
- Commit message format: \"fix(phase-$PHASE): description\"
- Do NOT push — the script handles pushing"

claude -p "$PROMPT" \
  --max-turns "$MAX_TURNS" \
  --allowedTools "Bash(bash tests/*)" "Bash(git add*)" "Bash(git commit*)" "Bash(git status)" "Bash(git diff*)" "Bash(mkdir*)" "Edit" "Read" "Write" "Glob" "Grep" \
  --disallowedTools "Bash(git push*)" "Bash(git reset*)" "Bash(rm -rf*)" \
  >> "$LOG_FILE" 2>&1

CLAUDE_EXIT=$?
ELAPSED=$(($(date +%s) - START_TIME))
log "Claude Code exited with: $CLAUDE_EXIT (elapsed: ${ELAPSED}s)"

# Step 4: Commit any uncommitted changes Claude left behind
if [ -n "$(git status --porcelain)" ]; then
  log "Claude left uncommitted changes. Committing..."
  git add -A
  git commit -m "fix(phase-$PHASE): dev loop auto-commit $DATE" >> "$LOG_FILE" 2>&1 || true
fi

# Step 5: Push if there are new commits
COMMITS_AHEAD=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
if [ "$COMMITS_AHEAD" -gt 0 ]; then
  log "Pushing $COMMITS_AHEAD new commit(s)..."
  git push origin main >> "$LOG_FILE" 2>&1 || {
    log "ERROR: git push failed. Will retry on next run."
  }
  log "Pushed successfully."
else
  log "No new commits to push."
fi

# Step 6: Post-development verification
log "Running post-development verification..."
POST_JSON=$(bash tests/identify-next-priority.sh 2>/dev/null)
POST_FAIL=$(echo "$POST_JSON" | grep -o '"fail": *[0-9]*' | tail -1 | sed 's/.*: *//')
POST_STATUS=$(echo "$POST_JSON" | grep -o '"status": *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')
POST_FAIL=${POST_FAIL:-0}

FIXED=$((TOTAL_FAIL - POST_FAIL))
if [ "$FIXED" -lt 0 ]; then FIXED=0; fi

ELAPSED=$(($(date +%s) - START_TIME))
log "Post-dev status: $POST_STATUS | Fixed: $FIXED | Remaining: $POST_FAIL | Duration: ${ELAPSED}s"
write_status "$POST_STATUS" "$PHASE" "$FIXED" "$POST_FAIL" "$ELAPSED"
log "═══ Dev Loop Complete ═══"
