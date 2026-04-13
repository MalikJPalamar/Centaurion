#!/usr/bin/env bash
# Centaurion — Phase 6: Cross-Venture Intelligence & System Coherence
# TDD: Tests written BEFORE implementation.
# Usage: bash tests/verify-coherence.sh

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
# R27: Cross-Venture Connections
# ============================================================
echo ""
echo "═══ R27: Cross-Venture Connections ═══"

# A document that explicitly maps connections between ventures
check_file_exists "docs/centaurion-wiki/cross-venture-map.md" \
  "R27.1: Cross-venture map exists"
check_file_contains "docs/centaurion-wiki/cross-venture-map.md" "AOB.*BuilderBee\|BuilderBee.*AOB" \
  "R27.2: Cross-venture map connects AOB ↔ BuilderBee"
check_file_contains "docs/centaurion-wiki/cross-venture-map.md" "Centaurion.*BuilderBee\|BuilderBee.*Centaurion" \
  "R27.3: Cross-venture map connects Centaurion ↔ BuilderBee"

# AOB wiki references BuilderBee patterns where applicable
check_file_contains "docs/aob-wiki/crm-migration.md" "builderbee\|ghl\|automation" \
  "R27.4: AOB CRM migration page references BuilderBee/GHL expertise"

# BuilderBee wiki references Centaurion methodology
check_file_contains "docs/builderbee-wiki/service-offerings.md" "centaurion\|framework\|active inference\|precision" \
  "R27.5: BuilderBee offerings reference Centaurion methodology"

# ============================================================
# R28: System Coherence Checks
# ============================================================
echo ""
echo "═══ R28: System Coherence ═══"

# CLAUDE.md and AGENTS.md should reference the same Three Laws text
CLAUDE_LAWS=$(grep -c "Hierarchy\|Routing\|Coupling" "$REPO_ROOT/CLAUDE.md" 2>/dev/null || echo "0")
AGENTS_LAWS=$(grep -c "Hierarchy\|Routing\|Coupling" "$REPO_ROOT/AGENTS.md" 2>/dev/null || echo "0")
if [ "$CLAUDE_LAWS" -ge 3 ] && [ "$AGENTS_LAWS" -ge 3 ]; then
  pass "R28.1: CLAUDE.md and AGENTS.md both reference all Three Laws"
else
  fail "R28.1: Laws not consistent across CLAUDE.md ($CLAUDE_LAWS) and AGENTS.md ($AGENTS_LAWS)"
fi

# All agent personalities reference the Three Laws
for agent in Cortex Nova Daemon; do
  check_file_contains "agents/$agent.md" "Three Laws\|Hierarchy\|Routing\|Coupling" \
    "R28.2: agents/$agent.md references the Three Laws"
done

# Memory configs are consistent — all three ventures tagged
check_file_contains "memory/supermemory.json" "aob" \
  "R28.3a: Supermemory has AOB container"
check_file_contains "memory/supermemory.json" "builderbee" \
  "R28.3b: Supermemory has BuilderBee container"
check_file_contains "memory/supermemory.json" "centaurion" \
  "R28.3c: Supermemory has Centaurion container"

# wiki-repos.json references all three wiki directories
check_file_contains "memory/wiki-repos.json" "aob-wiki" \
  "R28.4a: wiki-repos references aob-wiki"
check_file_contains "memory/wiki-repos.json" "builderbee-wiki" \
  "R28.4b: wiki-repos references builderbee-wiki"
check_file_contains "memory/wiki-repos.json" "centaurion-wiki" \
  "R28.4c: wiki-repos references centaurion-wiki"

# ============================================================
# R29: Documentation & Onboarding
# ============================================================
echo ""
echo "═══ R29: Documentation & Onboarding ═══"

# A getting-started guide for new sessions
check_file_exists "docs/getting-started.md" \
  "R29.1: Getting started guide exists"
check_file_contains "docs/getting-started.md" "CLAUDE.md\|clone\|install\|setup" \
  "R29.2: Getting started has setup instructions"

# Architecture diagram (text-based is fine)
check_file_exists "docs/architecture.md" \
  "R29.3: Architecture overview doc exists"
check_file_contains "docs/architecture.md" "Cortex\|Nova\|Daemon" \
  "R29.4: Architecture doc describes agent topology"
check_file_contains "docs/architecture.md" "Supermemory\|wiki\|memory" \
  "R29.5: Architecture doc describes memory layers"

# Changelog tracking what the dev loop has built
check_file_exists "CHANGELOG.md" \
  "R29.6: CHANGELOG.md exists"
check_file_contains "CHANGELOG.md" "Phase 1\|Phase 2\|Phase 3" \
  "R29.7: CHANGELOG tracks completed phases"

# ============================================================
# R30: Case Study — Centaurion as Its Own Client
# ============================================================
echo ""
echo "═══ R30: Case Study ═══"

check_file_exists "docs/case-studies/centaurion-as-client.md" \
  "R30.1: 'Centaurion as its own client' case study exists"
check_file_contains "docs/case-studies/centaurion-as-client.md" "precision ratio\|three laws\|active inference" \
  "R30.2: Case study references framework concepts"
check_file_contains "docs/case-studies/centaurion-as-client.md" "result\|outcome\|metric\|improvement" \
  "R30.3: Case study documents measurable outcomes"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 6 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 6 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 6 REQUIREMENT(S) PENDING"
  exit 1
fi
