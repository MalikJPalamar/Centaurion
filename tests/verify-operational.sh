#!/usr/bin/env bash
# Centaurion — Phase 5: Operational Workflows & Skills Maturity
# TDD: Tests written BEFORE implementation.
# Usage: bash tests/verify-operational.sh

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
check_file_contains() {
  if [ -f "$REPO_ROOT/$1" ] && grep -qi "$2" "$REPO_ROOT/$1"; then pass "$3"; else fail "$3 — pattern '$2' not in $1"; fi
}

# ============================================================
# R23: Skills Maturity — Each Skill Has Depth
# ============================================================
echo ""
echo "═══ R23: Skills Maturity ═══"

SKILLS="centaurion-core routing-gate weekly-review sa-scan gap-analysis"
for skill in $SKILLS; do
  FILE="$REPO_ROOT/skills/$skill/SKILL.md"
  if [ -f "$FILE" ]; then
    SIZE=$(wc -c < "$FILE")
    if [ "$SIZE" -ge 1000 ]; then
      pass "R23.1: skills/$skill/SKILL.md is substantial ($SIZE bytes)"
    else
      fail "R23.1: skills/$skill/SKILL.md too thin ($SIZE bytes, need ≥1000)"
    fi
  else
    fail "R23.1: skills/$skill/SKILL.md not found"
  fi
done

# Each skill should have examples
for skill in $SKILLS; do
  check_file_contains "skills/$skill/SKILL.md" "example\|e\.g\.\|for instance\|sample\|such as" \
    "R23.2: skills/$skill/SKILL.md contains examples"
done

# ============================================================
# R24: New Skills — Venture-Specific
# ============================================================
echo ""
echo "═══ R24: Venture-Specific Skills ═══"

check_file_exists "skills/aob-ops/SKILL.md" \
  "R24.1: AOB operations skill exists"
check_file_contains "skills/aob-ops/SKILL.md" "name:" \
  "R24.2: aob-ops has YAML frontmatter"
check_file_contains "skills/aob-ops/SKILL.md" "ontraport\|ghl\|crm\|mighty\|facilitator" \
  "R24.3: aob-ops references AOB-specific systems"

check_file_exists "skills/builderbee-delivery/SKILL.md" \
  "R24.4: BuilderBee delivery skill exists"
check_file_contains "skills/builderbee-delivery/SKILL.md" "name:" \
  "R24.5: builderbee-delivery has YAML frontmatter"
check_file_contains "skills/builderbee-delivery/SKILL.md" "ghl\|client\|automation\|onboarding" \
  "R24.6: builderbee-delivery references BB-specific workflows"

# ============================================================
# R25: Workflow Completeness
# ============================================================
echo ""
echo "═══ R25: Workflow Completeness ═══"

# Each workflow should have concrete steps, not just templates
check_file_contains "workflows/daily-health.md" "docker\|curl\|systemctl\|uptime\|ping" \
  "R25.1: daily-health.md has concrete monitoring commands"

check_file_contains "workflows/weekly-gap-analysis.md" "wiki\|cluster\|gap\|question" \
  "R25.2: weekly-gap-analysis.md has analysis procedure"

check_file_contains "workflows/centaurion-iteration.yaml" "sense\|predict\|route" \
  "R25.3: centaurion-iteration.yaml has loop phases"

# New workflows
check_file_exists "workflows/client-onboarding.md" \
  "R25.4: BuilderBee client onboarding workflow exists"
check_file_contains "workflows/client-onboarding.md" "ghl\|setup\|audit\|automation" \
  "R25.5: client-onboarding has concrete steps"

check_file_exists "workflows/aob-weekly-ops.md" \
  "R25.6: AOB weekly ops workflow exists"
check_file_contains "workflows/aob-weekly-ops.md" "crm\|membership\|support\|content" \
  "R25.7: aob-weekly-ops references operational areas"

# ============================================================
# R26: Framework Maturity — Cross-References
# ============================================================
echo ""
echo "═══ R26: Framework Cross-References ═══"

# Every framework file should reference at least 2 other framework files
FRAMEWORK_FILES=$(find "$REPO_ROOT/framework" -name "*.md" -type f)
CROSS_REF_OK=true
for f in $FRAMEWORK_FILES; do
  FNAME=$(basename "$f")
  OTHER_REFS=$(grep -coE 'framework/[a-z0-9-]+\.md' "$f" 2>/dev/null || echo "0")
  if [ "$OTHER_REFS" -lt 1 ]; then
    fail "R26.1: framework/$FNAME has no cross-references to other framework files"
    CROSS_REF_OK=false
  fi
done
if [ "$CROSS_REF_OK" = true ]; then
  pass "R26.1: All framework files have cross-references"
fi

# Index file for framework navigation
check_file_exists "framework/README.md" \
  "R26.2: framework/README.md index exists"
check_file_contains "framework/README.md" "precision-ratio\|three-laws\|active-inference" \
  "R26.3: framework/README.md links to key framework files"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 5 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 5 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 5 REQUIREMENT(S) PENDING"
  exit 1
fi
