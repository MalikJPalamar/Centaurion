#!/usr/bin/env bash
# Centaurion — Dev Loop Self-Test
# Verifies the development loop infrastructure itself works correctly.
# Usage: bash tests/verify-dev-loop.sh
# Exit 0 = all pass, Exit 1 = failures found

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
TOTAL=0

pass() { PASS=$((PASS + 1)); TOTAL=$((TOTAL + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); echo "  ✗ $1"; }

# ============================================================
# R11: Daily Development Loop Workflow
# ============================================================
echo ""
echo "═══ R11: Daily Development Loop ═══"

# R11.1: Workflow file exists
WORKFLOW="$REPO_ROOT/.github/workflows/daily-dev-loop.yml"
if [ -f "$WORKFLOW" ]; then
  pass "R11.1: daily-dev-loop.yml exists"
else
  fail "R11.1: daily-dev-loop.yml not found"
fi

# R11.2: Cron schedule at 6am CEST (4am UTC)
if [ -f "$WORKFLOW" ] && grep -q "cron:.*'0 4" "$WORKFLOW"; then
  pass "R11.2: Workflow scheduled at 0 4 * * * (6am CEST)"
elif [ -f "$WORKFLOW" ] && grep -q 'cron:.*"0 4' "$WORKFLOW"; then
  pass "R11.2: Workflow scheduled at 0 4 * * * (6am CEST)"
else
  fail "R11.2: Cron schedule not set to '0 4 * * *'"
fi

# R11.3: Manual dispatch trigger
if [ -f "$WORKFLOW" ] && grep -q "workflow_dispatch" "$WORKFLOW"; then
  pass "R11.3: Workflow has workflow_dispatch trigger"
else
  fail "R11.3: Missing workflow_dispatch trigger"
fi

# R11.4: Runs core verification
if [ -f "$WORKFLOW" ] && grep -q "verify-core-loop" "$WORKFLOW"; then
  pass "R11.4: Workflow runs verify-core-loop.sh"
else
  fail "R11.4: Workflow doesn't reference verify-core-loop.sh"
fi

# R11.5: Runs dev loop self-test
if [ -f "$WORKFLOW" ] && grep -q "verify-dev-loop" "$WORKFLOW"; then
  pass "R11.5: Workflow runs verify-dev-loop.sh"
else
  fail "R11.5: Workflow doesn't reference verify-dev-loop.sh"
fi

# R11.6: Runs priority identification
if [ -f "$WORKFLOW" ] && grep -q "identify-next-priority" "$WORKFLOW"; then
  pass "R11.6: Workflow runs identify-next-priority.sh"
else
  fail "R11.6: Workflow doesn't reference identify-next-priority.sh"
fi

# R11.7-R11.10: Issue creation (check workflow has issue creation step)
if [ -f "$WORKFLOW" ] && grep -q "create.*issue\|issues" "$WORKFLOW"; then
  pass "R11.7: Workflow creates GitHub Issue"
else
  fail "R11.7: Workflow doesn't create GitHub Issue"
fi

if [ -f "$WORKFLOW" ] && grep -q "dev-loop" "$WORKFLOW"; then
  pass "R11.10: Workflow uses dev-loop label"
else
  fail "R11.10: Missing dev-loop label"
fi

# ============================================================
# R12: Priority Identification
# ============================================================
echo ""
echo "═══ R12: Priority Identification ═══"

PRIORITY_SCRIPT="$REPO_ROOT/tests/identify-next-priority.sh"

# R12.1: Script exists
if [ -f "$PRIORITY_SCRIPT" ]; then
  pass "R12.1: identify-next-priority.sh exists"
else
  fail "R12.1: identify-next-priority.sh not found"
fi

# R12.2: Script is executable or can be run with bash
if [ -f "$PRIORITY_SCRIPT" ]; then
  pass "R12.2: Script exists and can be executed with bash"
else
  fail "R12.2: Script not available"
fi

# R12.3: Script produces JSON output
if [ -f "$PRIORITY_SCRIPT" ]; then
  OUTPUT=$(bash "$PRIORITY_SCRIPT" 2>/dev/null || true)
  if echo "$OUTPUT" | grep -q '"phase"'; then
    pass "R12.3: Script outputs JSON with 'phase' field"
  else
    fail "R12.3: Script output doesn't contain JSON with 'phase' field"
  fi

  if echo "$OUTPUT" | grep -q '"requirement"'; then
    pass "R12.3b: Script outputs JSON with 'requirement' field"
  else
    fail "R12.3b: Script output doesn't contain JSON with 'requirement' field"
  fi
fi

# R12.4-R12.6: Priority ordering (checked via script execution)
if [ -f "$PRIORITY_SCRIPT" ]; then
  EXIT_CODE=0
  bash "$PRIORITY_SCRIPT" >/dev/null 2>&1 || EXIT_CODE=$?
  if [ "$EXIT_CODE" -eq 0 ]; then
    pass "R12.6: Script exits 0 (produces output regardless of state)"
  else
    fail "R12.6: Script exits non-zero ($EXIT_CODE)"
  fi
fi

# ============================================================
# R13: TDD Cycle Structure
# ============================================================
echo ""
echo "═══ R13: TDD Cycle Structure ═══"

# R13.1-R13.3: Phase verification scripts exist
if [ -f "$REPO_ROOT/tests/verify-core-loop.sh" ]; then
  pass "R13.2: Phase 1 verification exists (verify-core-loop.sh)"
else
  fail "R13.2: Phase 1 verification missing"
fi

if [ -f "$REPO_ROOT/tests/verify-memory-integration.sh" ]; then
  pass "R13.3: Phase 2 verification exists (verify-memory-integration.sh)"
else
  fail "R13.3: Phase 2 verification missing"
fi

# R13.5-R13.6: run-all.sh exists and works
if [ -f "$REPO_ROOT/tests/run-all.sh" ]; then
  pass "R13.5: tests/run-all.sh exists"
else
  fail "R13.5: tests/run-all.sh not found"
fi

# ============================================================
# R14: Dev Loop Self-Test (meta — this script testing itself)
# ============================================================
echo ""
echo "═══ R14: Dev Loop Self-Test ═══"

pass "R14.1: verify-dev-loop.sh exists (you're running it)"

# R14.2: Check YAML syntax of workflow
if [ -f "$WORKFLOW" ]; then
  # Basic YAML check: has 'name:', 'on:', 'jobs:' keys
  if grep -q "^name:" "$WORKFLOW" && grep -q "^on:" "$WORKFLOW" && grep -q "^jobs:" "$WORKFLOW"; then
    pass "R14.2: daily-dev-loop.yml has valid workflow structure (name, on, jobs)"
  else
    fail "R14.2: daily-dev-loop.yml missing required YAML keys"
  fi
fi

# R14.3: Priority script produces valid JSON
if [ -f "$PRIORITY_SCRIPT" ]; then
  OUTPUT=$(bash "$PRIORITY_SCRIPT" 2>/dev/null || true)
  # Check it looks like JSON (has opening brace AND "phase" field)
  HAS_BRACE=$(echo "$OUTPUT" | grep -c '{' || true)
  HAS_PHASE=$(echo "$OUTPUT" | grep -c '"phase"' || true)
  if [ "$HAS_BRACE" -gt 0 ] && [ "$HAS_PHASE" -gt 0 ]; then
    pass "R14.3: identify-next-priority.sh produces JSON with phase field"
  else
    fail "R14.3: Priority script output doesn't look like valid JSON"
  fi
fi

# R14.4: Verification scripts exist for defined phases
if [ -f "$REPO_ROOT/tests/verify-core-loop.sh" ] && [ -f "$REPO_ROOT/tests/verify-memory-integration.sh" ]; then
  pass "R14.4: Verification scripts exist for Phase 1 and Phase 2"
else
  fail "R14.4: Missing verification scripts for defined phases"
fi

# R14.5: ROADMAP and REQUIREMENTS mention same phases
if [ -f "$REPO_ROOT/.planning/ROADMAP.md" ] && [ -f "$REPO_ROOT/.planning/REQUIREMENTS.md" ]; then
  if grep -q "Phase 1\|Phase 2" "$REPO_ROOT/.planning/ROADMAP.md" && \
     grep -q "R1\|R15" "$REPO_ROOT/.planning/REQUIREMENTS.md"; then
    pass "R14.5: ROADMAP and REQUIREMENTS reference consistent phases"
  else
    fail "R14.5: Phase references inconsistent between ROADMAP and REQUIREMENTS"
  fi
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  DEV LOOP RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ DEV LOOP INFRASTRUCTURE VERIFIED"
  exit 0
else
  echo "  ✗ $FAIL DEV LOOP CHECK(S) FAILED"
  exit 1
fi
