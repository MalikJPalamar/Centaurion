#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Daily Development Loop — VPS1 Cron Script
# ═══════════════════════════════════════════════════════════
#
# Runs Claude Code against failing tests using Max subscription.
# Scheduled via cron at 6am CET on VPS1.
#
# Install:
#   1. Clone repo:  git clone https://github.com/MalikJPalamar/Centaurion.git ~/centaurion
#   2. Auth Claude:  claude auth login
#   3. Install cron: bash deploy/vps1/centaurion-dev-loop.sh --install
#   4. Done. Runs daily at 6am CET.
#
# Manual run:
#   bash deploy/vps1/centaurion-dev-loop.sh
#
# Logs:
#   ~/centaurion/logs/dev-loop-YYYY-MM-DD.log
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$HOME/centaurion}"
LOG_DIR="$REPO_DIR/logs"
DATE=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/dev-loop-$DATE.log"
MAX_TURNS=15
MAX_FIXES=3

# ── Install mode ──────────────────────────────────────────
if [ "${1:-}" = "--install" ]; then
  # 6am CET = 4am UTC (CEST, summer) or 5am UTC (CET, winter)
  # Using 4am UTC for summer. Adjust if needed.
  CRON_LINE="0 4 * * * cd $REPO_DIR && bash deploy/vps1/centaurion-dev-loop.sh >> $LOG_DIR/cron.log 2>&1"

  mkdir -p "$LOG_DIR"

  # Add to crontab if not already there
  if crontab -l 2>/dev/null | grep -q "centaurion-dev-loop"; then
    echo "Cron job already installed. Current entry:"
    crontab -l | grep "centaurion-dev-loop"
  else
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "Cron job installed:"
    echo "  $CRON_LINE"
  fi

  echo ""
  echo "Verify with: crontab -l | grep centaurion"
  echo "Logs will be at: $LOG_DIR/"
  echo ""
  echo "Prerequisites:"
  echo "  1. Claude Code authenticated: claude auth login"
  echo "  2. Git push access: git push origin main (test it)"
  echo "  3. Repo cloned at: $REPO_DIR"
  exit 0
fi

# ── Uninstall mode ────────────────────────────────────────
if [ "${1:-}" = "--uninstall" ]; then
  crontab -l 2>/dev/null | grep -v "centaurion-dev-loop" | crontab -
  echo "Cron job removed."
  exit 0
fi

# ── Main execution ────────────────────────────────────────
mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "═══ Centaurion Dev Loop Starting ═══"
log "Date: $DATE"
log "Repo: $REPO_DIR"

# Step 1: Pull latest
log "Pulling latest from main..."
cd "$REPO_DIR"
git pull origin main >> "$LOG_FILE" 2>&1 || {
  log "ERROR: git pull failed"
  exit 1
}

# Step 2: Run tests and identify priority
log "Running test suite..."
PRIORITY_JSON=$(bash tests/identify-next-priority.sh 2>/dev/null)
STATUS=$(echo "$PRIORITY_JSON" | grep -o '"status": *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')
PHASE=$(echo "$PRIORITY_JSON" | grep -o '"phase": *[0-9]*' | head -1 | sed 's/.*: *//')
FIRST_FAIL=$(echo "$PRIORITY_JSON" | grep -o '"first_failure": *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')
TOTAL_FAIL=$(echo "$PRIORITY_JSON" | grep -o '"fail": *[0-9]*' | tail -1 | sed 's/.*: *//')

log "Status: $STATUS | Phase: $PHASE | Failures: ${TOTAL_FAIL:-0}"

if [ "$STATUS" = "all_passing" ]; then
  log "All tests passing. Nothing to develop."
  log "═══ Dev Loop Complete (no work needed) ═══"
  exit 0
fi

log "First failure: $FIRST_FAIL"

# Step 3: Run Claude Code to fix failing tests
log "Running Claude Code (Max subscription)..."

PROMPT="You are the Centaurion daily development loop. Read CLAUDE.md for context.

## Current State
$(echo "$PRIORITY_JSON")

## Your Task (TDD Green Step)
1. Read the failing test file to understand EXACTLY what it checks
2. Read the relevant source file(s) that need to change
3. Make the MINIMUM change to turn the failing test green
4. Run the specific phase test to verify your fix works
5. Run \`bash tests/run-all.sh\` to check for regressions
6. If all earlier phase tests still pass, stage and commit your changes
7. Do NOT fix more than $MAX_FIXES failing tests per run

## Constraints
- All content is markdown + JSON. No TypeScript, no compilation.
- Follow patterns in existing files (YAML frontmatter for skills, etc.)
- Do NOT commit API keys or secrets
- Do NOT modify test files — only modify implementation files
- Commit message format: \"fix(phase-$PHASE): description\"
- Do NOT push — the script handles pushing after you finish"

claude -p "$PROMPT" \
  --max-turns "$MAX_TURNS" \
  --allowedTools "Bash(bash tests/*)" "Bash(git add*)" "Bash(git commit*)" "Bash(git status)" "Bash(git diff*)" "Bash(mkdir*)" "Edit" "Read" "Write" "Glob" "Grep" \
  --disallowedTools "Bash(git push*)" "Bash(git reset*)" "Bash(rm -rf*)" \
  >> "$LOG_FILE" 2>&1

CLAUDE_EXIT=$?
log "Claude Code exited with: $CLAUDE_EXIT"

# Step 4: Push if there are new commits
COMMITS_AHEAD=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
if [ "$COMMITS_AHEAD" -gt 0 ]; then
  log "Pushing $COMMITS_AHEAD new commit(s)..."
  git push origin main >> "$LOG_FILE" 2>&1 || {
    log "ERROR: git push failed"
    exit 1
  }
  log "Pushed successfully."
else
  log "No new commits to push."
fi

# Step 5: Post-development verification
log "Running post-development verification..."
POST_JSON=$(bash tests/identify-next-priority.sh 2>/dev/null)
POST_FAIL=$(echo "$POST_JSON" | grep -o '"fail": *[0-9]*' | tail -1 | sed 's/.*: *//')
POST_STATUS=$(echo "$POST_JSON" | grep -o '"status": *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')

log "Post-dev status: $POST_STATUS | Remaining failures: ${POST_FAIL:-0}"
log "═══ Dev Loop Complete ═══"
