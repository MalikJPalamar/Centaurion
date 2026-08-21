#!/usr/bin/env bash
# Centaurion — MemoryBridgeExtension dependency-injection verification
# Confirms the bridge to centaurion_core.detect_venture is a typed, visible dep
# (not a hidden lazy import).
# Usage: bash tests/verify-memory-bridge-di.sh
# Exit 0 = all pass, Exit 1 = failures found

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXT_DIR="$REPO_ROOT/omega/extensions"
PASS=0
FAIL=0
TOTAL=0

pass() { PASS=$((PASS + 1)); TOTAL=$((TOTAL + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); echo "  ✗ $1"; }

echo ""
echo "═══ MemoryBridgeExtension DI ═══"

# D1: import is at module top (visible to AST/IDE/type-checker)
if grep -q "^from centaurion_core import detect_venture" "$EXT_DIR/memory_bridge.py"; then
  pass "D1: detect_venture imported at module top"
else
  fail "D1: detect_venture not imported at module top in memory_bridge.py"
fi

# D2: no lazy import remains inside on_message
if grep -q "^[[:space:]]\+from centaurion_core import" "$EXT_DIR/memory_bridge.py"; then
  fail "D2: lazy import of centaurion_core still present inside a method body"
else
  pass "D2: no lazy import of centaurion_core inside method bodies"
fi

# D3: no import cycle — both modules import cleanly together
if PYTHONPATH="$EXT_DIR" python3 -c "import memory_bridge, centaurion_core" 2>/dev/null; then
  pass "D3: memory_bridge + centaurion_core import together (no cycle)"
else
  fail "D3: import cycle detected between memory_bridge and centaurion_core"
fi

# D4: __init__ accepts a custom classifier
INIT_CHECK=$(PYTHONPATH="$EXT_DIR" python3 -c "
import inspect, memory_bridge
sig = inspect.signature(memory_bridge.MemoryBridgeExtension.__init__)
print('classify' in sig.parameters)
" 2>/dev/null || echo "False")
if [ "$INIT_CHECK" = "True" ]; then
  pass "D4: MemoryBridgeExtension.__init__ accepts a 'classify' parameter"
else
  fail "D4: MemoryBridgeExtension.__init__ missing 'classify' parameter"
fi

# D5: injected classifier is actually used on_message
DI_CHECK=$(PYTHONPATH="$EXT_DIR" python3 -c "
import memory_bridge
calls = []
class M: content = 'test message'
ext = memory_bridge.MemoryBridgeExtension(agent=None, classify=lambda t: calls.append(t) or 'aob')
ext.on_message(M())
print(calls == ['test message'] and ext.session_venture == 'aob')
" 2>/dev/null || echo "False")
if [ "$DI_CHECK" = "True" ]; then
  pass "D5: injected classifier is called by on_message and sets session_venture"
else
  fail "D5: injected classifier not used by on_message"
fi

# D6: default behavior unchanged — real detect_venture still produces same tags
DEFAULT_CHECK=$(PYTHONPATH="$EXT_DIR" python3 -c "
import memory_bridge
class M: content = 'working on Art of Breath facilitator certification'
ext = memory_bridge.MemoryBridgeExtension(agent=None)
ext.on_message(M())
print(ext.session_venture)
" 2>/dev/null || echo "ERR")
if [ "$DEFAULT_CHECK" = "aob" ]; then
  pass "D6: default classifier still detects venture correctly (aob)"
else
  fail "D6: default classifier broken — got '$DEFAULT_CHECK', expected 'aob'"
fi

echo ""
echo "════════════════════════════════════════"
echo "  MEMORY-BRIDGE DI RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL CHECKS PASS"
  exit 0
else
  echo "  ✗ $FAIL CHECK(S) FAILED"
  exit 1
fi
