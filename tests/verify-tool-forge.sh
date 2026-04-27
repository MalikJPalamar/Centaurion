#!/usr/bin/env bash
# Centaurion Phase 14 — Tool Forge Verification
# Verifies dynamic tool creation: scaffold → sandbox exec → promotion gate
# Usage: bash tests/verify-tool-forge.sh
# Exit 0 = all pass, Exit 1 = failures found

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
TOTAL=0

pass() { PASS=$((PASS + 1)); TOTAL=$((TOTAL + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); echo "  ✗ $1"; }

check_file_exists() {
  if [ -f "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — not found: $1"; fi
}

check_dir_exists() {
  if [ -d "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — dir not found: $1"; fi
}

check_file_contains() {
  local file="$1" pattern="$2" desc="$3"
  if [ -f "$REPO_ROOT/$file" ] && grep -qi "$pattern" "$REPO_ROOT/$file"; then
    pass "$desc"
  else
    fail "$desc — pattern '$pattern' missing in $file"
  fi
}

# ============================================================
# F1 · Source files exist
# ============================================================
echo ""
echo "═══ F1: Source files ═══"

check_file_exists "centaurion/extensions/sandbox.py" "F1.1: sandbox.py exists"
check_file_exists "centaurion/extensions/tool_forge.py" "F1.2: tool_forge.py exists"
check_file_exists "centaurion/extensions/routing_gate.py" "F1.3: routing_gate.py exists"
check_file_exists "centaurion/extensions/__init__.py" "F1.4: extensions package init exists"

# ============================================================
# F2 · Directory structure
# ============================================================
echo ""
echo "═══ F2: Directory structure ═══"

check_dir_exists "skills/auto-generated/_staging" "F2.1: _staging/ exists"
check_dir_exists "skills/auto-generated/_promoted" "F2.2: _promoted/ exists"
check_dir_exists "skills/auto-generated/_failed" "F2.3: _failed/ exists"
check_dir_exists "skills/auto-generated/.template" "F2.4: .template/ exists"
check_file_exists "skills/auto-generated/.template/SKILL.md" "F2.5: template SKILL.md exists"
check_file_exists "skills/auto-generated/README.md" "F2.6: auto-generated README exists"

# ============================================================
# F3 · Routing Gate has tool_creation event taxonomy
# ============================================================
echo ""
echo "═══ F3: Routing Gate tool_creation events ═══"

check_file_contains "centaurion/extensions/routing_gate.py" \
  "TOOL_CREATION_EVENTS" "F3.1: TOOL_CREATION_EVENTS taxonomy defined"
check_file_contains "centaurion/extensions/routing_gate.py" \
  "classify_tool_creation" "F3.2: classify_tool_creation function defined"
check_file_contains "centaurion/extensions/routing_gate.py" \
  "scaffold" "F3.3: scaffold event type"
check_file_contains "centaurion/extensions/routing_gate.py" \
  "sandbox_exec" "F3.4: sandbox_exec event type"
check_file_contains "centaurion/extensions/routing_gate.py" \
  "promote" "F3.5: promote event type"

# ============================================================
# F4 · Sandbox safety properties
# ============================================================
echo ""
echo "═══ F4: Sandbox safety properties ═══"

check_file_contains "centaurion/extensions/sandbox.py" \
  "network.*none" "F4.1: network off by default"
check_file_contains "centaurion/extensions/sandbox.py" \
  "cap-drop" "F4.2: drops Linux capabilities"
check_file_contains "centaurion/extensions/sandbox.py" \
  "no-new-privileges" "F4.3: no privilege escalation"
check_file_contains "centaurion/extensions/sandbox.py" \
  "read-only" "F4.4: read-only root filesystem"
check_file_contains "centaurion/extensions/sandbox.py" \
  "memory" "F4.5: memory cap set"
check_file_contains "centaurion/extensions/sandbox.py" \
  "Worktree" "F4.6: Worktree primitive present"

# ============================================================
# F5 · Tool Forge three-tier flow
# ============================================================
echo ""
echo "═══ F5: Tool Forge three-tier flow ═══"

check_file_contains "centaurion/extensions/tool_forge.py" \
  "def scaffold" "F5.1: scaffold method defined"
check_file_contains "centaurion/extensions/tool_forge.py" \
  "def execute" "F5.2: execute method defined"
check_file_contains "centaurion/extensions/tool_forge.py" \
  "def propose_promotion" "F5.3: propose_promotion method defined"
check_file_contains "centaurion/extensions/tool_forge.py" \
  "def approve" "F5.4: approve method defined"
check_file_contains "centaurion/extensions/tool_forge.py" \
  "def reject" "F5.5: reject method defined"
check_file_contains "centaurion/extensions/tool_forge.py" \
  "tool-creation-log.jsonl" "F5.6: writes to tool-creation-log.jsonl"

# ============================================================
# F6 · Pytest suite passes
# ============================================================
echo ""
echo "═══ F6: Pytest suite ═══"

if command -v python3 >/dev/null 2>&1; then
  if python3 -m pytest --version >/dev/null 2>&1; then
    if (cd "$REPO_ROOT" && python3 -m pytest tests/test_sandbox.py tests/test_tool_forge.py tests/test_routing_gate.py -q --no-header 2>&1 | tail -5 | grep -qE "passed"); then
      pass "F6.1: pytest suite green (test_sandbox + test_tool_forge + test_routing_gate)"
    else
      fail "F6.1: pytest suite has failures"
    fi
  else
    fail "F6.1: pytest not installed (python3 -m pytest)"
  fi
else
  fail "F6.1: python3 not available"
fi

# ============================================================
# F7 · End-to-end forge demo
# ============================================================
echo ""
echo "═══ F7: End-to-end forge demo ═══"

DEMO_OUT=$(cd "$REPO_ROOT" && python3 -c "
import json, sys, tempfile, subprocess
from pathlib import Path
sys.path.insert(0, '.')
from centaurion.extensions.sandbox import MockSandbox
from centaurion.extensions.tool_forge import ToolForge, PromotionDecision

with tempfile.TemporaryDirectory() as td:
    repo = Path(td)
    subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=repo, check=True)
    for k, v in [('user.email', 't@x'), ('user.name', 'T'),
                 ('commit.gpgsign', 'false'), ('tag.gpgsign', 'false')]:
        subprocess.run(['git', 'config', k, v], cwd=repo, check=True)
    (repo / 'README.md').write_text('init')
    subprocess.run(['git', 'add', '-A'], cwd=repo, check=True)
    subprocess.run(['git', 'commit', '-q', '-m', 'init'], cwd=repo, check=True)

    sb = MockSandbox(exit_code=0, stdout='ok')
    forge = ToolForge(repo=repo, sandbox=sb)
    s = forge.scaffold('demo_tool', 'demo', 'def f(): return 1\n',
                       'from impl import f; assert f() == 1\n')
    ex = forge.execute(s)
    assert ex.passed, 'execution should pass'
    prop = forge.propose_promotion(s, ex)
    assert prop.route == 'surface_to_human', 'promote must surface'
    forge.approve(prop)
    promoted = repo / 'skills' / 'auto-generated' / '_promoted' / 'demo_tool'
    assert (promoted / 'SKILL.md').exists(), 'promotion did not write SKILL.md'
    assert (promoted / 'impl.py').exists(), 'promotion did not write impl.py'
    log = repo / 'memory' / 'state' / 'tool-creation-log.jsonl'
    events = [json.loads(l)['event'] for l in log.read_text().splitlines() if l]
    assert events == ['scaffold', 'sandbox_exec', 'promote', 'approve'], events
    print('OK')
" 2>&1)

if echo "$DEMO_OUT" | grep -q "^OK$"; then
  pass "F7.1: end-to-end forge demo (scaffold → exec → propose → approve)"
else
  fail "F7.1: end-to-end demo failed: $DEMO_OUT"
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "═══ Summary ═══"
echo "  Passed: $PASS / $TOTAL"
echo "  Failed: $FAIL / $TOTAL"

if [ "$FAIL" -eq 0 ]; then
  echo ""
  echo "✓ Phase 14 verified: Tool Forge ready"
  exit 0
else
  echo ""
  echo "✗ Phase 14 has $FAIL failure(s)"
  exit 1
fi
