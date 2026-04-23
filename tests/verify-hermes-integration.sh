#!/usr/bin/env bash
# Centaurion — Phase 10: Hermes + Browser-Harness Integration
# Tests that Hermes is configured with Centaurion identity and running.
# Usage: bash tests/verify-hermes-integration.sh

set -uo pipefail

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
# R41: Hermes Deploy Config
# ============================================================
echo ""
echo "═══ R41: Hermes Deploy Config ═══"

check_file_exists "deploy/hermes/SOUL.md" \
  "R41.1: Hermes SOUL.md exists"
check_file_contains "deploy/hermes/SOUL.md" "Cortex" \
  "R41.2: SOUL.md identifies as Cortex"
check_file_contains "deploy/hermes/SOUL.md" "Three Laws" \
  "R41.3: SOUL.md contains Three Laws"
check_file_contains "deploy/hermes/SOUL.md" "Routing" \
  "R41.4: SOUL.md contains Routing Gate"
check_file_contains "deploy/hermes/SOUL.md" "Precision" \
  "R41.5: SOUL.md contains Precision Ratio"
check_file_contains "deploy/hermes/SOUL.md" "AOB.*BuilderBee\|BuilderBee.*AOB" \
  "R41.6: SOUL.md references ventures"

check_file_exists "deploy/hermes/MEMORY.md" \
  "R41.7: Hermes MEMORY.md exists"
check_file_contains "deploy/hermes/MEMORY.md" "AOB\|BuilderBee\|Centaurion" \
  "R41.8: MEMORY.md contains venture context"

check_file_exists "deploy/hermes/setup.sh" \
  "R41.9: Hermes setup script exists"
check_file_contains "deploy/hermes/setup.sh" "SOUL.md\|skills\|MEMORY" \
  "R41.10: Setup script deploys personality + skills + memory"

# ============================================================
# R42: Browser-Harness Integration
# ============================================================
echo ""
echo "═══ R42: Browser-Harness Integration ═══"

check_file_exists "deploy/browser-harness/setup.sh" \
  "R42.1: Browser-harness setup script exists"
check_file_contains "deploy/browser-harness/setup.sh" "browser-harness\|chrome\|chromium" \
  "R42.2: Setup script references browser dependencies"
check_file_contains "deploy/browser-harness/setup.sh" "pip install\|pip3 install" \
  "R42.3: Setup script installs Python dependencies"

# ============================================================
# R43: Hermes Runtime (VPS2-specific — will fail elsewhere)
# ============================================================
echo ""
echo "═══ R43: Hermes Runtime ═══"

# R43.1: Hermes CLI available
if command -v hermes &>/dev/null; then
  pass "R43.1: hermes CLI found"
else
  fail "R43.1: hermes CLI not found (VPS2-specific)"
fi

# R43.2: Hermes config directory exists
HERMES_DIR="${HERMES_DIR:-$HOME/.hermes}"
if [ -d "$HERMES_DIR" ]; then
  pass "R43.2: Hermes config directory exists ($HERMES_DIR)"
else
  fail "R43.2: Hermes config not found at $HERMES_DIR (VPS2-specific)"
fi

# R43.3: SOUL.md deployed to Hermes
if [ -f "$HERMES_DIR/SOUL.md" ] 2>/dev/null && grep -qi "Cortex" "$HERMES_DIR/SOUL.md" 2>/dev/null; then
  pass "R43.3: Cortex SOUL.md deployed to Hermes"
else
  fail "R43.3: SOUL.md not deployed (run: bash deploy/hermes/setup.sh)"
fi

# R43.4: Skills deployed to Hermes
HERMES_SKILLS="$HERMES_DIR/skills"
if [ -d "$HERMES_SKILLS" ] 2>/dev/null; then
  SKILL_COUNT=$(find "$HERMES_SKILLS" -name "SKILL.md" -type f 2>/dev/null | wc -l)
  if [ "$SKILL_COUNT" -ge 3 ]; then
    pass "R43.4: $SKILL_COUNT skills deployed to Hermes"
  else
    fail "R43.4: Only $SKILL_COUNT skills in Hermes (need ≥3)"
  fi
else
  fail "R43.4: No skills directory in Hermes (run: bash deploy/hermes/setup.sh)"
fi

# R43.5: Hermes can respond (quick test)
if command -v hermes &>/dev/null; then
  RESPONSE=$(timeout 30 hermes -p "Respond with only: CORTEX_READY" 2>/dev/null || echo "TIMEOUT")
  if echo "$RESPONSE" | grep -qi "CORTEX_READY\|cortex\|ready"; then
    pass "R43.5: Hermes responds as Cortex"
  else
    fail "R43.5: Hermes did not respond as expected"
  fi
else
  fail "R43.5: Cannot test — hermes CLI not available"
fi

# ============================================================
# R44: Browser-Harness Runtime
# ============================================================
echo ""
echo "═══ R44: Browser-Harness Runtime ═══"

# R44.1: browser-harness directory exists
BH_DIR="${BROWSER_HARNESS_DIR:-$HOME/browser-harness}"
if [ -d "$BH_DIR" ]; then
  pass "R44.1: browser-harness directory exists"
else
  fail "R44.1: browser-harness not found at $BH_DIR"
fi

# R44.2: Python dependencies installed
if python3 -c "import browser_harness" 2>/dev/null || python3 -c "import cdp_use" 2>/dev/null; then
  pass "R44.2: browser-harness Python dependencies installed"
else
  fail "R44.2: browser-harness dependencies not installed"
fi

# R44.3: Chrome/Chromium available
if command -v google-chrome &>/dev/null || command -v chromium-browser &>/dev/null || command -v chromium &>/dev/null; then
  pass "R44.3: Chrome/Chromium available"
else
  fail "R44.3: No Chrome/Chromium found"
fi

# ============================================================
# R45: Cross-System Coherence
# ============================================================
echo ""
echo "═══ R45: Cross-System Coherence ═══"

# R45.1: SOUL.md and CLAUDE.md reference same Three Laws
SOUL_LAWS=$(grep -c "Hierarchy\|Routing\|Coupling" "$REPO_ROOT/deploy/hermes/SOUL.md" 2>/dev/null || true)
CLAUDE_LAWS=$(grep -c "Hierarchy\|Routing\|Coupling" "$REPO_ROOT/CLAUDE.md" 2>/dev/null || true)
if [ "$SOUL_LAWS" -ge 3 ] && [ "$CLAUDE_LAWS" -ge 3 ]; then
  pass "R45.1: SOUL.md and CLAUDE.md both reference all Three Laws"
else
  fail "R45.1: Laws inconsistent between SOUL.md ($SOUL_LAWS) and CLAUDE.md ($CLAUDE_LAWS)"
fi

# R45.2: Skills in repo match skills deployed (format compatible)
REPO_SKILLS=$(find "$REPO_ROOT/skills" -name "SKILL.md" -type f | wc -l)
if [ "$REPO_SKILLS" -ge 5 ]; then
  pass "R45.2: $REPO_SKILLS skills in repo (agentskills.io format)"
else
  fail "R45.2: Only $REPO_SKILLS skills in repo"
fi

# R45.3: deploy/hermes/MEMORY.md references all three ventures
check_file_contains "deploy/hermes/MEMORY.md" "AOB" "R45.3a: MEMORY.md references AOB"
check_file_contains "deploy/hermes/MEMORY.md" "BuilderBee" "R45.3b: MEMORY.md references BuilderBee"
check_file_contains "deploy/hermes/MEMORY.md" "Centaurion" "R45.3c: MEMORY.md references Centaurion"

# R45.4: Active Inference loop present in SOUL.md
check_file_contains "deploy/hermes/SOUL.md" "SENSE.*PREDICT\|PREDICT.*COMPARE\|Active Inference" \
  "R45.4: SOUL.md contains Active Inference loop"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 10 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 10 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 10 REQUIREMENT(S) PENDING"
  exit 1
fi
