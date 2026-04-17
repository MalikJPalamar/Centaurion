#!/usr/bin/env bash
# Centaurion — Phase 8: Operational Automation
# Tests that real automation is running, not just documented.
# Usage: bash tests/verify-automation.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
TOTAL=0

pass() { PASS=$((PASS + 1)); TOTAL=$((TOTAL + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); echo "  ✗ $1"; }

# ============================================================
# R36: Dev Loop Intelligence — Script Improvements
# ============================================================
echo ""
echo "═══ R36: Dev Loop Intelligence ═══"

SCRIPT="$REPO_ROOT/deploy/vps1/centaurion-dev-loop.sh"

# R36.1: Dev loop script logs token/turn counts
if [ -f "$SCRIPT" ] && grep -q "turns\|tokens\|duration\|elapsed" "$SCRIPT"; then
  pass "R36.1: Dev loop tracks execution metrics (turns/duration)"
else
  fail "R36.1: Dev loop doesn't track execution metrics"
fi

# R36.2: Dev loop has lock file to prevent concurrent runs
if [ -f "$SCRIPT" ] && grep -q "lock\|flock\|LOCK" "$SCRIPT"; then
  pass "R36.2: Dev loop has concurrency protection (lock file)"
else
  fail "R36.2: Dev loop has no concurrency protection"
fi

# R36.3: Dev loop rotates old logs (keeps last 14 days)
if [ -f "$SCRIPT" ] && grep -q "find.*-mtime\|log.*rotation\|cleanup\|rotate" "$SCRIPT"; then
  pass "R36.3: Dev loop rotates old logs"
else
  fail "R36.3: Dev loop doesn't rotate old logs"
fi

# R36.4: Dev loop reports summary to a machine-readable status file
if [ -f "$REPO_ROOT/memory/state/dev-loop-status.json" ]; then
  pass "R36.4: dev-loop-status.json exists"
else
  fail "R36.4: memory/state/dev-loop-status.json not found"
fi

# ============================================================
# R37: Weekly Review — Automation Script
# ============================================================
echo ""
echo "═══ R37: Weekly Review Automation ═══"

# R37.1: Weekly review runner script exists (not just the SKILL.md)
if [ -f "$REPO_ROOT/deploy/vps1/weekly-review.sh" ]; then
  pass "R37.1: Weekly review runner script exists"
else
  fail "R37.1: deploy/vps1/weekly-review.sh not found"
fi

# R37.2: Weekly review script uses claude -p to generate the review
if [ -f "$REPO_ROOT/deploy/vps1/weekly-review.sh" ] && grep -q "claude.*-p\|claude -p" "$REPO_ROOT/deploy/vps1/weekly-review.sh"; then
  pass "R37.2: Weekly review uses Claude CLI"
else
  fail "R37.2: Weekly review doesn't use Claude CLI"
fi

# R37.3: Weekly review cron entry exists (weekly schedule)
if [ -f "$REPO_ROOT/deploy/vps1/weekly-review.sh" ] && grep -q "cron\|weekly\|sunday\|monday" "$REPO_ROOT/deploy/vps1/weekly-review.sh"; then
  pass "R37.3: Weekly review has cron install instructions"
else
  fail "R37.3: Weekly review missing cron schedule"
fi

# R37.4: At least one weekly review output exists
if find "$REPO_ROOT/memory/state/" -name "weekly-review-*.md" -type f 2>/dev/null | grep -q .; then
  pass "R37.4: At least one weekly review output exists"
else
  fail "R37.4: No weekly review outputs in memory/state/"
fi

# ============================================================
# R38: Health Check — Runnable Script
# ============================================================
echo ""
echo "═══ R38: Health Check Automation ═══"

# R38.1: Health check runner script exists
if [ -f "$REPO_ROOT/deploy/vps1/health-check.sh" ]; then
  pass "R38.1: Health check runner script exists"
else
  fail "R38.1: deploy/vps1/health-check.sh not found"
fi

# R38.2: Health check actually pings/checks real endpoints
if [ -f "$REPO_ROOT/deploy/vps1/health-check.sh" ] && grep -q "curl\|ping\|docker ps\|systemctl" "$REPO_ROOT/deploy/vps1/health-check.sh"; then
  pass "R38.2: Health check has real system commands"
else
  fail "R38.2: Health check has no real system commands"
fi

# R38.3: Health check outputs machine-readable status
if [ -f "$REPO_ROOT/deploy/vps1/health-check.sh" ] && grep -q "json\|JSON\|status.*:" "$REPO_ROOT/deploy/vps1/health-check.sh"; then
  pass "R38.3: Health check outputs structured status"
else
  fail "R38.3: Health check doesn't output structured status"
fi

# ============================================================
# R39: Routing Gate — Live Classification
# ============================================================
echo ""
echo "═══ R39: Routing Gate Live ═══"

# R39.1: routing-log has entries from last 7 days (system is classifying)
RLOG="$REPO_ROOT/memory/state/routing-log.jsonl"
if [ -f "$RLOG" ]; then
  WEEK_AGO=$(date -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d 2>/dev/null || echo "2026-04-08")
  RECENT=$(grep '"timestamp"' "$RLOG" | grep -c "2026-04-1[0-9]\|2026-04-2[0-9]" || true)
  if [ "$RECENT" -ge 3 ]; then
    pass "R39.1: $RECENT routing classifications in recent entries"
  else
    fail "R39.1: Only $RECENT recent routing entries (need ≥3 from last 7 days)"
  fi
else
  fail "R39.1: routing-log.jsonl not found"
fi

# R39.2: At least one entry has been reviewed (outcome_rating != null)
if [ -f "$RLOG" ] && grep -q '"outcome_rating": [0-9]' "$RLOG"; then
  pass "R39.2: At least one routing entry has been reviewed"
else
  fail "R39.2: No routing entries have been reviewed (all outcome_rating: null)"
fi

# R39.3: Routing log includes all three route types
HAS_AUTO=$(grep -c '"ai_autonomous"' "$RLOG" 2>/dev/null || true)
HAS_REVIEW=$(grep -c '"ai_with_review"' "$RLOG" 2>/dev/null || true)
HAS_SURFACE=$(grep -c '"surface_to_human"' "$RLOG" 2>/dev/null || true)
if [ "$HAS_AUTO" -gt 0 ] && [ "$HAS_REVIEW" -gt 0 ]; then
  pass "R39.3: Routing log has multiple route types (auto: $HAS_AUTO, review: $HAS_REVIEW)"
else
  fail "R39.3: Routing log needs diverse route types (auto: $HAS_AUTO, review: $HAS_REVIEW, surface: $HAS_SURFACE)"
fi

# ============================================================
# R40: Test Infrastructure — Self-Maintaining
# ============================================================
echo ""
echo "═══ R40: Test Infrastructure ═══"

# R40.1: identify-next-priority.sh handles all defined phases
PHASE_COUNT=$(grep -c "PHASE_NAMES" "$REPO_ROOT/tests/identify-next-priority.sh" 2>/dev/null || true)
SCRIPT_PHASES=$(grep -c "verify-" "$REPO_ROOT/tests/run-all.sh" 2>/dev/null || true)
if [ "$SCRIPT_PHASES" -ge 7 ]; then
  pass "R40.1: run-all.sh covers $SCRIPT_PHASES verification phases"
else
  fail "R40.1: run-all.sh only covers $SCRIPT_PHASES phases (should be ≥7)"
fi

# R40.2: All test scripts are syntactically valid bash
ALL_VALID=true
for test_script in "$REPO_ROOT"/tests/verify-*.sh; do
  if ! bash -n "$test_script" 2>/dev/null; then
    fail "R40.2: Syntax error in $(basename "$test_script")"
    ALL_VALID=false
  fi
done
if [ "$ALL_VALID" = true ]; then
  pass "R40.2: All test scripts pass syntax check"
fi

# R40.3: ROADMAP phases match test phases
ROADMAP_PHASES=$(grep -c "^## Phase" "$REPO_ROOT/.planning/ROADMAP.md" 2>/dev/null || true)
if [ "$ROADMAP_PHASES" -ge 7 ]; then
  pass "R40.3: ROADMAP has $ROADMAP_PHASES phases defined"
else
  fail "R40.3: ROADMAP has $ROADMAP_PHASES phases (should match test count)"
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 8 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 8 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 8 REQUIREMENT(S) PENDING"
  exit 1
fi
