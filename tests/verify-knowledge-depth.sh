#!/usr/bin/env bash
# Centaurion — Phase 4: Knowledge Depth & Wiki Expansion
# TDD: Tests written BEFORE implementation.
# Usage: bash tests/verify-knowledge-depth.sh

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
check_dir_min_files() {
  local dir="$1" min="$2" desc="$3"
  if [ -d "$REPO_ROOT/$dir" ]; then
    COUNT=$(find "$REPO_ROOT/$dir" -name "*.md" -type f | wc -l)
    if [ "$COUNT" -ge "$min" ]; then
      pass "$desc ($COUNT files)"
    else
      fail "$desc — has $COUNT, need ≥$min"
    fi
  else
    fail "$desc — directory not found: $dir"
  fi
}

# ============================================================
# R19: Wiki Depth — centaurion-wiki (≥10 pages)
# ============================================================
echo ""
echo "═══ R19: Centaurion Wiki Depth ═══"

check_dir_min_files "docs/centaurion-wiki" 10 \
  "R19.1: centaurion-wiki has ≥10 pages"

# Required topic pages
check_file_exists "docs/centaurion-wiki/five-sensing-layers.md" \
  "R19.2: Wiki page: five-sensing-layers"
check_file_exists "docs/centaurion-wiki/markov-blanket.md" \
  "R19.3: Wiki page: markov-blanket"
check_file_exists "docs/centaurion-wiki/11-levels.md" \
  "R19.4: Wiki page: 11-levels agentic engineering"
check_file_exists "docs/centaurion-wiki/named-agents.md" \
  "R19.5: Wiki page: named agents (Cortex, Nova, Daemon)"
check_file_exists "docs/centaurion-wiki/memory-architecture.md" \
  "R19.6: Wiki page: three-layer memory architecture"
check_file_exists "docs/centaurion-wiki/ventures.md" \
  "R19.7: Wiki page: three ventures overview"

# Cross-linking between wiki pages
check_file_contains "docs/centaurion-wiki/three-laws.md" "precision-ratio\|active-inference\|routing-gate" \
  "R19.8: three-laws.md cross-links to other wiki pages"
check_file_contains "docs/centaurion-wiki/active-inference-loop.md" "three-laws\|precision-ratio\|routing-gate" \
  "R19.9: active-inference-loop.md cross-links to other wiki pages"

# ============================================================
# R20: AOB Wiki Foundation
# ============================================================
echo ""
echo "═══ R20: AOB Wiki Foundation ═══"

check_file_exists "docs/aob-wiki/README.md" \
  "R20.1: aob-wiki README exists"
check_dir_min_files "docs/aob-wiki" 5 \
  "R20.2: aob-wiki has ≥5 pages"
check_file_exists "docs/aob-wiki/crm-migration.md" \
  "R20.3: Wiki page: CRM migration (Ontraport → GHL)"
check_file_exists "docs/aob-wiki/team.md" \
  "R20.4: Wiki page: AOB team and roles"
check_file_exists "docs/aob-wiki/facilitator-certification.md" \
  "R20.5: Wiki page: facilitator certification program"
check_file_exists "docs/aob-wiki/tech-stack.md" \
  "R20.6: Wiki page: AOB tech stack"

# ============================================================
# R21: BuilderBee Wiki Foundation
# ============================================================
echo ""
echo "═══ R21: BuilderBee Wiki Foundation ═══"

check_file_exists "docs/builderbee-wiki/README.md" \
  "R21.1: builderbee-wiki README exists"
check_dir_min_files "docs/builderbee-wiki" 5 \
  "R21.2: builderbee-wiki has ≥5 pages"
check_file_exists "docs/builderbee-wiki/ghl-playbook.md" \
  "R21.3: Wiki page: GoHighLevel playbook"
check_file_exists "docs/builderbee-wiki/client-onboarding.md" \
  "R21.4: Wiki page: client onboarding workflow"
check_file_exists "docs/builderbee-wiki/service-offerings.md" \
  "R21.5: Wiki page: service offerings"
check_file_exists "docs/builderbee-wiki/ai-automation-patterns.md" \
  "R21.6: Wiki page: AI automation patterns"

# ============================================================
# R22: Identity Depth
# ============================================================
echo ""
echo "═══ R22: Identity Depth ═══"

# Each identity file should be substantial (≥500 bytes)
for f in PURPOSE MISSION GOALS CHALLENGES CONTACTS BELIEFS MODELS PREFERENCES HISTORY OPINIONS; do
  FILE="$REPO_ROOT/identity/$f.md"
  if [ -f "$FILE" ]; then
    SIZE=$(wc -c < "$FILE")
    if [ "$SIZE" -ge 500 ]; then
      pass "R22.1: identity/$f.md is substantial ($SIZE bytes)"
    else
      fail "R22.1: identity/$f.md too thin ($SIZE bytes, need ≥500)"
    fi
  else
    fail "R22.1: identity/$f.md not found"
  fi
done

# GOALS.md should reference current phase
check_file_contains "identity/GOALS.md" "Phase 4\|Phase 5\|knowledge\|wiki" \
  "R22.2: GOALS.md references current/upcoming work"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 4 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 4 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 4 REQUIREMENT(S) PENDING"
  exit 1
fi
