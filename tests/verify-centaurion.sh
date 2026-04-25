#!/usr/bin/env bash
# Centaurion — Phase 11: Centaurion Integration
# Verifies the Centaurion stack (Centaurion + Hermes + browser-harness + Pi)
# Usage: bash tests/verify-centaurion.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
TOTAL=0

pass() { PASS=$((PASS + 1)); TOTAL=$((TOTAL + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); echo "  ✗ $1"; }

check_file_exists() {
  if [ -f "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — not found: $1"; fi
}
check_file_contains() {
  if [ -f "$REPO_ROOT/$1" ] && grep -qi "$2" "$REPO_ROOT/$1"; then pass "$3"; else fail "$3"; fi
}
check_python_syntax() {
  if [ -f "$REPO_ROOT/$1" ] && python3 -c "import py_compile; py_compile.compile('$REPO_ROOT/$1', doraise=True)" 2>/dev/null; then
    pass "$2"
  else
    fail "$2 — syntax error in $1"
  fi
}

# ============================================================
# R46: Centaurion Architecture
# ============================================================
echo ""
echo "═══ R46: Centaurion Architecture ═══"

check_file_exists "CENTAURION.md" "R46.1: CENTAURION.md architecture spec exists"
check_file_contains "CENTAURION.md" "Hermes" "R46.2: CENTAURION.md references Hermes engine"
check_file_contains "CENTAURION.md" "browser-harness" "R46.3: CENTAURION.md references browser-harness"
check_file_contains "CENTAURION.md" "Three Laws" "R46.4: CENTAURION.md preserves Three Laws"
check_file_contains "CENTAURION.md" "Precision Ratio" "R46.5: CENTAURION.md preserves Precision Ratio"

# ============================================================
# R47: Centaurion Core Extension
# ============================================================
echo ""
echo "═══ R47: Centaurion Core Extension ═══"

check_file_exists "centaurion/extensions/centaurion_core.py" "R47.1: centaurion_core.py exists"
check_python_syntax "centaurion/extensions/centaurion_core.py" "R47.2: centaurion_core.py valid Python"
check_file_contains "centaurion/extensions/centaurion_core.py" "load_identity" "R47.3: Has identity loading function"
check_file_contains "centaurion/extensions/centaurion_core.py" "detect_venture" "R47.4: Has venture detection"
check_file_contains "centaurion/extensions/centaurion_core.py" "session_start" "R47.5: Hooks into session_start"
check_file_contains "centaurion/extensions/centaurion_core.py" "Three Laws\|TELOS\|identity" "R47.6: References Centaurion identity system"

# ============================================================
# R48: Routing Gate Extension
# ============================================================
echo ""
echo "═══ R48: Routing Gate Extension ═══"

check_file_exists "centaurion/extensions/routing_gate.py" "R48.1: routing_gate.py exists"
check_python_syntax "centaurion/extensions/routing_gate.py" "R48.2: routing_gate.py valid Python"
check_file_contains "centaurion/extensions/routing_gate.py" "classify_tool_call" "R48.3: Has tool call classification"
check_file_contains "centaurion/extensions/routing_gate.py" "0.7" "R48.4: Novelty threshold 0.7"
check_file_contains "centaurion/extensions/routing_gate.py" "0.5" "R48.5: Stakes threshold 0.5"
check_file_contains "centaurion/extensions/routing_gate.py" "surface_to_human" "R48.6: Can block and surface to human"
check_file_contains "centaurion/extensions/routing_gate.py" "on_tool_call" "R48.7: Intercepts tool calls via Hermes hook"
check_file_contains "centaurion/extensions/routing_gate.py" "routing-log" "R48.8: Logs to routing-log.jsonl"

# ============================================================
# R49: Browser-Harness Tool
# ============================================================
echo ""
echo "═══ R49: Browser-Harness Tool ═══"

check_file_exists "centaurion/tools/browser_harness.py" "R49.1: browser_harness.py exists"
check_python_syntax "centaurion/tools/browser_harness.py" "R49.2: browser_harness.py valid Python"
check_file_contains "centaurion/tools/browser_harness.py" "browser_navigate" "R49.3: Has navigate function"
check_file_contains "centaurion/tools/browser_harness.py" "browser_screenshot" "R49.4: Has screenshot function"
check_file_contains "centaurion/tools/browser_harness.py" "register_tools" "R49.5: Has tool registration function"
check_file_contains "centaurion/tools/browser_harness.py" "TOOLS" "R49.6: Has tool catalog"

# ============================================================
# R50: Centaurion SOUL & Config
# ============================================================
echo ""
echo "═══ R50: Centaurion SOUL & Config ═══"

check_file_exists "centaurion/SOUL.md" "R50.1: Centaurion SOUL.md exists"
check_file_contains "centaurion/SOUL.md" "Cortex" "R50.2: SOUL.md identifies as Cortex"
check_file_contains "centaurion/SOUL.md" "Three Laws" "R50.3: SOUL.md has Three Laws"
check_file_contains "centaurion/SOUL.md" "Self-Improvement\|self-improv\|skill" "R50.4: SOUL.md enables self-improvement"
check_file_contains "centaurion/SOUL.md" "browser" "R50.5: SOUL.md lists browser tools"
check_file_contains "centaurion/SOUL.md" "AOB.*BuilderBee\|ventures" "R50.6: SOUL.md has venture context"

check_file_exists "centaurion/install.sh" "R50.7: Centaurion installer exists"
check_file_contains "centaurion/install.sh" "hermes" "R50.8: Installer deploys to Hermes"
check_file_contains "centaurion/install.sh" "SOUL.md\|extensions\|skills" "R50.9: Installer covers personality + extensions + skills"

# ============================================================
# R51: Cross-System Coherence
# ============================================================
echo ""
echo "═══ R51: Cross-System Coherence ═══"

# Centaurion SOUL.md and CLAUDE.md both have Three Laws
CENTAURION_LAWS=$(grep -c "Hierarchy\|Routing\|Coupling" "$REPO_ROOT/centaurion/SOUL.md" 2>/dev/null || true)
CLAUDE_LAWS=$(grep -c "Hierarchy\|Routing\|Coupling" "$REPO_ROOT/CLAUDE.md" 2>/dev/null || true)
if [ "$CENTAURION_LAWS" -ge 3 ] && [ "$CLAUDE_LAWS" -ge 3 ]; then
  pass "R51.1: Centaurion SOUL.md and CLAUDE.md both have all Three Laws"
else
  fail "R51.1: Laws inconsistent (SOUL: $CENTAURION_LAWS, CLAUDE: $CLAUDE_LAWS)"
fi

# Extensions reference Centaurion repo path
check_file_contains "centaurion/extensions/centaurion_core.py" "CENTAURION_REPO" "R51.2: Core extension references repo path"
check_file_contains "centaurion/extensions/routing_gate.py" "CENTAURION_REPO" "R51.3: Routing gate references repo path"

# Browser tool references browser-harness dir
check_file_contains "centaurion/tools/browser_harness.py" "BROWSER_HARNESS_DIR" "R51.4: Browser tool references harness directory"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 11 (CENTAURION) RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL CENTAURION REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL CENTAURION REQUIREMENT(S) PENDING"
  exit 1
fi
