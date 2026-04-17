#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Weekly Review — L2 Sensing Layer
# ═══════════════════════════════════════════════════════════
#
# Runs Claude Code to generate a structured weekly comparison.
# Analyzes ratings trends, routing accuracy, wiki growth,
# and cross-venture patterns.
#
# Schedule via cron (Mondays 7am CET = 5am UTC):
#   0 5 * * 1 cd ~/Centaurion && CENTAURION_REPO=~/Centaurion bash deploy/vps1/weekly-review.sh >> ~/Centaurion/logs/cron.log 2>&1
#
# Manual run:
#   CENTAURION_REPO=~/Centaurion bash deploy/vps1/weekly-review.sh
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$HOME/Centaurion}"
LOG_DIR="$REPO_DIR/logs"
STATE_DIR="$REPO_DIR/memory/state"
DATE=$(date +%Y-%m-%d)
WEEK=$(date +%YW%V)
OUTPUT_FILE="$STATE_DIR/weekly-review-$WEEK.md"
LOG_FILE="$LOG_DIR/weekly-review-$DATE.log"

mkdir -p "$LOG_DIR" "$STATE_DIR"

log() {
  echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "═══ Weekly Review Starting ═══"
log "Week: $WEEK | Output: $OUTPUT_FILE"

cd "$REPO_DIR"
git pull origin main >> "$LOG_FILE" 2>&1 || true

# Gather data for the prompt
RATINGS_DATA=""
if [ -f "$STATE_DIR/ratings.jsonl" ]; then
  RATINGS_DATA=$(cat "$STATE_DIR/ratings.jsonl")
fi

ROUTING_DATA=""
if [ -f "$STATE_DIR/routing-log.jsonl" ]; then
  ROUTING_DATA=$(cat "$STATE_DIR/routing-log.jsonl")
fi

WIKI_COUNTS=""
for wiki in docs/centaurion-wiki docs/aob-wiki docs/builderbee-wiki; do
  if [ -d "$REPO_DIR/$wiki" ]; then
    COUNT=$(find "$REPO_DIR/$wiki" -name "*.md" -type f | wc -l)
    WIKI_COUNTS="$WIKI_COUNTS\n$wiki: $COUNT pages"
  fi
done

TEST_RESULTS=$(bash tests/run-all.sh 2>&1 | tail -20)
GIT_LOG=$(git log --oneline --since="7 days ago" 2>/dev/null | head -20)

PROMPT="You are Cortex running the weekly review (L2 sensing). Read skills/weekly-review/SKILL.md for the procedure.

## Data for This Week

### Ratings (memory/state/ratings.jsonl):
$RATINGS_DATA

### Routing Log (memory/state/routing-log.jsonl):
$ROUTING_DATA

### Wiki Page Counts:
$(echo -e "$WIKI_COUNTS")

### Test Suite Results:
$TEST_RESULTS

### Git Activity (last 7 days):
$GIT_LOG

## Your Task
Generate a weekly review following the format in skills/weekly-review/SKILL.md.
Write the output as a markdown file. Focus on:
1. Rating trends (improving, declining, stable?)
2. Routing accuracy (correct classifications?)
3. Wiki growth (new pages? stale areas?)
4. Dev loop productivity (tests fixed per run?)
5. Cross-venture patterns
6. Recommended adjustments for next week

Output the review to stdout — the script will save it."

REVIEW=$(claude -p "$PROMPT" --max-turns 5 2>>"$LOG_FILE")

if [ -n "$REVIEW" ]; then
  echo "$REVIEW" > "$OUTPUT_FILE"
  log "Review written to: $OUTPUT_FILE"

  git add "$OUTPUT_FILE"
  git commit -m "review(weekly): $WEEK L2 sensing — structured comparison" >> "$LOG_FILE" 2>&1 || true
  git push origin main >> "$LOG_FILE" 2>&1 || log "Push failed — will retry"
  log "Review committed and pushed."
else
  log "ERROR: Claude returned empty review"
fi

log "═══ Weekly Review Complete ═══"
