#!/usr/bin/env bash
# Centaurion — Identify Next Development Priority
# Reads verification results and outputs the highest-priority failing requirement.
# Used by the daily dev loop to plan the next iteration.
# Output: JSON with phase, requirement, description, test_file, tdd_plan
# Exit 0 always (reports status even when everything passes)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --- Run each phase's verification and capture results ---

# Phase 1: Core Loop
P1_OUTPUT=""
P1_EXIT=0
P1_OUTPUT=$(bash "$REPO_ROOT/tests/verify-core-loop.sh" 2>&1) || P1_EXIT=$?
P1_PASS=$(echo "$P1_OUTPUT" | grep -c "  ✓" || true)
P1_FAIL=$(echo "$P1_OUTPUT" | grep -c "  ✗" || true)
P1_TOTAL=$((P1_PASS + P1_FAIL))

# Phase 2: Memory Integration
P2_OUTPUT=""
P2_EXIT=0
P2_OUTPUT=$(bash "$REPO_ROOT/tests/verify-memory-integration.sh" 2>&1) || P2_EXIT=$?
P2_PASS=$(echo "$P2_OUTPUT" | grep -c "  ✓" || true)
P2_FAIL=$(echo "$P2_OUTPUT" | grep -c "  ✗" || true)
P2_TOTAL=$((P2_PASS + P2_FAIL))

# Phase 3: Multi-Runtime & Feedback
P3_OUTPUT=""
P3_EXIT=0
P3_OUTPUT=$(bash "$REPO_ROOT/tests/verify-multi-runtime.sh" 2>&1) || P3_EXIT=$?
P3_PASS=$(echo "$P3_OUTPUT" | grep -c "  ✓" || true)
P3_FAIL=$(echo "$P3_OUTPUT" | grep -c "  ✗" || true)
P3_TOTAL=$((P3_PASS + P3_FAIL))

# Overall
TOTAL_PASS=$((P1_PASS + P2_PASS + P3_PASS))
TOTAL_FAIL=$((P1_FAIL + P2_FAIL + P3_FAIL))
TOTAL_ALL=$((TOTAL_PASS + TOTAL_FAIL))

# --- Determine next priority ---

if [ "$P1_FAIL" -gt 0 ]; then
  # Phase 1 has failures — fix these first
  FIRST_FAIL=$(echo "$P1_OUTPUT" | grep "  ✗" | head -1 | sed 's/.*✗ //')
  REQ_ID=$(echo "$FIRST_FAIL" | grep -oE 'R[0-9]+\.[0-9]+' | head -1 || echo "R?")
  REQ_GROUP=$(echo "$REQ_ID" | grep -oE 'R[0-9]+' | head -1 || echo "R?")

  cat <<PRIORITY_JSON
{
  "status": "failing",
  "phase": 1,
  "phase_name": "Core Loop",
  "requirement": "$REQ_GROUP",
  "first_failure": "$FIRST_FAIL",
  "test_file": "tests/verify-core-loop.sh",
  "phase1": {"pass": $P1_PASS, "fail": $P1_FAIL, "total": $P1_TOTAL},
  "phase2": {"pass": $P2_PASS, "fail": $P2_FAIL, "total": $P2_TOTAL},
  "overall": {"pass": $TOTAL_PASS, "fail": $TOTAL_FAIL, "total": $TOTAL_ALL},
  "tdd_plan": {
    "red": "Phase 1 test failing: $FIRST_FAIL",
    "green": "Fix the implementation to make this test pass",
    "refactor": "Re-run full suite to check for regressions"
  }
}
PRIORITY_JSON

elif [ "$P2_FAIL" -gt 0 ]; then
  FIRST_FAIL=$(echo "$P2_OUTPUT" | grep "  ✗" | head -1 | sed 's/.*✗ //')
  REQ_ID=$(echo "$FIRST_FAIL" | grep -oE 'R[0-9]+\.[0-9]+' | head -1 || echo "R?")
  REQ_GROUP=$(echo "$REQ_ID" | grep -oE 'R[0-9]+' | head -1 || echo "R?")

  cat <<PRIORITY_JSON
{
  "status": "progressing",
  "phase": 2,
  "phase_name": "Memory Integration",
  "requirement": "$REQ_GROUP",
  "first_failure": "$FIRST_FAIL",
  "test_file": "tests/verify-memory-integration.sh",
  "phase1": {"pass": $P1_PASS, "fail": $P1_FAIL, "total": $P1_TOTAL},
  "phase2": {"pass": $P2_PASS, "fail": $P2_FAIL, "total": $P2_TOTAL},
  "phase3": {"pass": $P3_PASS, "fail": $P3_FAIL, "total": $P3_TOTAL},
  "overall": {"pass": $TOTAL_PASS, "fail": $TOTAL_FAIL, "total": $TOTAL_ALL},
  "tdd_plan": {
    "red": "Phase 2 test failing: $FIRST_FAIL",
    "green": "Implement the feature to make this test pass",
    "refactor": "Re-run full suite to check for regressions"
  }
}
PRIORITY_JSON

elif [ "$P3_FAIL" -gt 0 ]; then
  FIRST_FAIL=$(echo "$P3_OUTPUT" | grep "  ✗" | head -1 | sed 's/.*✗ //')
  REQ_ID=$(echo "$FIRST_FAIL" | grep -oE 'R[0-9]+\.[0-9]+' | head -1 || echo "R?")
  REQ_GROUP=$(echo "$REQ_ID" | grep -oE 'R[0-9]+' | head -1 || echo "R?")

  cat <<PRIORITY_JSON
{
  "status": "progressing",
  "phase": 3,
  "phase_name": "Multi-Runtime and Feedback",
  "requirement": "$REQ_GROUP",
  "first_failure": "$FIRST_FAIL",
  "test_file": "tests/verify-multi-runtime.sh",
  "phase1": {"pass": $P1_PASS, "fail": $P1_FAIL, "total": $P1_TOTAL},
  "phase2": {"pass": $P2_PASS, "fail": $P2_FAIL, "total": $P2_TOTAL},
  "phase3": {"pass": $P3_PASS, "fail": $P3_FAIL, "total": $P3_TOTAL},
  "overall": {"pass": $TOTAL_PASS, "fail": $TOTAL_FAIL, "total": $TOTAL_ALL},
  "tdd_plan": {
    "red": "Phase 3 test failing: $FIRST_FAIL",
    "green": "Implement the feature to make this test pass",
    "refactor": "Re-run full suite to check for regressions"
  }
}
PRIORITY_JSON

else
  cat <<PRIORITY_JSON
{
  "status": "all_passing",
  "phase": 4,
  "phase_name": "Next: Knowledge Graph",
  "requirement": "none_failing",
  "first_failure": null,
  "test_file": null,
  "phase1": {"pass": $P1_PASS, "fail": $P1_FAIL, "total": $P1_TOTAL},
  "phase2": {"pass": $P2_PASS, "fail": $P2_FAIL, "total": $P2_TOTAL},
  "phase3": {"pass": $P3_PASS, "fail": $P3_FAIL, "total": $P3_TOTAL},
  "overall": {"pass": $TOTAL_PASS, "fail": $TOTAL_FAIL, "total": $TOTAL_ALL},
  "tdd_plan": {
    "red": "Write Phase 4 verification tests",
    "green": "Implement Phase 4 requirements to make tests pass",
    "refactor": "Review and optimize existing implementations"
  }
}
PRIORITY_JSON

fi

exit 0
