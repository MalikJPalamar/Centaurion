#!/usr/bin/env bash
# Centaurion — Phase 2: Memory Integration Verification
# TDD: Written BEFORE implementation. Expected to FAIL until Phase 2 is built.
# Usage: bash tests/verify-memory-integration.sh
# Exit 0 = all pass, Exit 1 = failures found

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
TOTAL=0

pass() { PASS=$((PASS + 1)); TOTAL=$((TOTAL + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); echo "  ✗ $1"; }

check_file_exists() {
  if [ -f "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — file not found: $1"; fi
}
check_file_nonempty() {
  if [ -f "$REPO_ROOT/$1" ] && [ -s "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — missing or empty: $1"; fi
}
check_file_contains() {
  if [ -f "$REPO_ROOT/$1" ] && grep -qi "$2" "$REPO_ROOT/$1"; then pass "$3"; else fail "$3 — pattern '$2' not found in $1"; fi
}
check_json_field() {
  local file="$1" field="$2" value="$3" desc="$4"
  if [ -f "$REPO_ROOT/$file" ] && grep -q "\"$field\".*\"$value\"" "$REPO_ROOT/$file"; then
    pass "$desc"
  else
    fail "$desc — field '$field' not set to '$value' in $file"
  fi
}
check_dir_exists() {
  if [ -d "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — directory not found: $1"; fi
}

# ============================================================
# R15: Memory Integration
# ============================================================
echo ""
echo "═══ R15: Memory Integration ═══"

# R15.1: Supermemory status = connected
check_json_field "memory/supermemory.json" "status" "connected" \
  "R15.1: supermemory.json status is 'connected'"

# R15.2: At least one wiki repo with status: active
if [ -f "$REPO_ROOT/memory/wiki-repos.json" ] && grep -q '"status".*"active"' "$REPO_ROOT/memory/wiki-repos.json"; then
  pass "R15.2: At least one wiki repo with status 'active'"
else
  fail "R15.2: No wiki repo with status 'active' in wiki-repos.json"
fi

# R15.3: Ratings state file exists
check_file_exists "memory/state/ratings.jsonl" \
  "R15.3: memory/state/ratings.jsonl exists for outcome ratings"

# R15.4: Routing log state file exists
check_file_exists "memory/state/routing-log.jsonl" \
  "R15.4: memory/state/routing-log.jsonl exists for routing decisions"

# R15.5: Core skill references Supermemory in SENSE
check_file_contains "skills/centaurion-core/SKILL.md" "supermemory" \
  "R15.5: centaurion-core SKILL.md references Supermemory recall"

# R15.6: Core skill references memory write in REMEMBER
check_file_contains "skills/centaurion-core/SKILL.md" "remember" \
  "R15.6: centaurion-core SKILL.md references REMEMBER/memory write"

# R15.7: Wiki content exists with at least 3 pages
WIKI_DIR="$REPO_ROOT/docs/centaurion-wiki"
if [ -d "$WIKI_DIR" ]; then
  WIKI_COUNT=$(find "$WIKI_DIR" -name "*.md" -type f | wc -l)
  if [ "$WIKI_COUNT" -ge 3 ]; then
    pass "R15.7: centaurion-wiki has $WIKI_COUNT pages (≥3 required)"
  else
    fail "R15.7: centaurion-wiki has $WIKI_COUNT pages (need ≥3)"
  fi
else
  fail "R15.7: docs/centaurion-wiki/ directory not found"
fi

# R15.8: CLAUDE.md REMEMBER step references Supermemory
check_file_contains "CLAUDE.md" "supermemory" \
  "R15.8: CLAUDE.md REMEMBER step references Supermemory"

# ============================================================
# R16: Feedback Infrastructure
# ============================================================
echo ""
echo "═══ R16: Feedback Infrastructure ═══"

# R16.1: daily-health.md references actual monitoring
check_file_contains "workflows/daily-health.md" "endpoint\|curl\|api\|health" \
  "R16.1: daily-health.md references monitoring endpoints"

# R16.2: memory/state/ directory exists with initialized files
check_dir_exists "memory/state" \
  "R16.2: memory/state/ directory exists"

# R16.3: Weekly review references ratings data source
check_file_contains "skills/weekly-review/SKILL.md" "ratings" \
  "R16.3: weekly-review references ratings data"

# R16.4: Feedback capture workflow exists
check_file_exists "workflows/feedback-capture.md" \
  "R16.4: workflows/feedback-capture.md exists"

# R16.5: Routing gate documents threshold adjustment with examples
check_file_contains "framework/routing-gate.md" "adjustment\|adjust" \
  "R16.5a: routing-gate.md documents threshold adjustment"
check_file_contains "framework/routing-gate.md" "example\|e\.g\.\|for instance" \
  "R16.5b: routing-gate.md includes adjustment examples"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 2 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 2 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 2 REQUIREMENT(S) PENDING"
  echo "  (This is expected until Phase 2 implementation)"
  exit 1
fi
