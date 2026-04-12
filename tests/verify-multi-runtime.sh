#!/usr/bin/env bash
# Centaurion — Phase 3: Multi-Runtime & Feedback Verification
# TDD: Written BEFORE implementation. Expected to FAIL until Phase 3 is built.
# Usage: bash tests/verify-multi-runtime.sh

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
check_dir_exists() {
  if [ -d "$REPO_ROOT/$1" ]; then pass "$2"; else fail "$2 — dir not found: $1"; fi
}

# ============================================================
# R17: Multi-Runtime Deployment Configs
# ============================================================
echo ""
echo "═══ R17: Multi-Runtime Deployment ═══"

# R17.1: Pi scaffold config exists
check_file_exists "deploy/pi/settings.json" \
  "R17.1: Pi scaffold settings.json exists"

# R17.2: Pi config references centaurion skills
check_file_contains "deploy/pi/settings.json" "centaurion" \
  "R17.2: Pi config references centaurion skills"

# R17.3: OpenClaw deploy config exists
check_file_exists "deploy/openclaw/SOUL.md" \
  "R17.3: OpenClaw SOUL.md deploy config exists"

# R17.4: OpenClaw SOUL.md matches Nova personality
check_file_contains "deploy/openclaw/SOUL.md" "Nova" \
  "R17.4: OpenClaw SOUL.md uses Nova personality"

# R17.5: Agent Zero config exists
check_file_exists "deploy/agent-zero/system-prompt.md" \
  "R17.5: Agent Zero system prompt exists"

# R17.6: Agent Zero references Three Laws
check_file_contains "deploy/agent-zero/system-prompt.md" "Three Laws\|Hierarchy.*Routing.*Coupling" \
  "R17.6: Agent Zero system prompt includes Three Laws"

# R17.7: Deploy directory has README with instructions
check_file_exists "deploy/README.md" \
  "R17.7: deploy/README.md with deployment instructions exists"

# ============================================================
# R18: Feedback Loop Infrastructure
# ============================================================
echo ""
echo "═══ R18: Feedback Loop Infrastructure ═══"

# R18.1: Daily health workflow references actual check commands
check_file_contains "workflows/daily-health.md" "curl\|docker\|systemctl\|ping\|status" \
  "R18.1: daily-health.md has concrete check commands"

# R18.2: Routing log has at least one sample entry (beyond schema line)
if [ -f "$REPO_ROOT/memory/state/routing-log.jsonl" ]; then
  LINES=$(wc -l < "$REPO_ROOT/memory/state/routing-log.jsonl")
  if [ "$LINES" -ge 2 ]; then
    pass "R18.2: routing-log.jsonl has sample entries"
  else
    fail "R18.2: routing-log.jsonl needs sample entries (only $LINES lines)"
  fi
else
  fail "R18.2: routing-log.jsonl not found"
fi

# R18.3: Ratings file has at least one sample entry
if [ -f "$REPO_ROOT/memory/state/ratings.jsonl" ]; then
  LINES=$(wc -l < "$REPO_ROOT/memory/state/ratings.jsonl")
  if [ "$LINES" -ge 2 ]; then
    pass "R18.3: ratings.jsonl has sample entries"
  else
    fail "R18.3: ratings.jsonl needs sample entries (only $LINES lines)"
  fi
else
  fail "R18.3: ratings.jsonl not found"
fi

# R18.4: centaurion-wiki has at least 6 pages (expanding knowledge base)
WIKI_DIR="$REPO_ROOT/docs/centaurion-wiki"
if [ -d "$WIKI_DIR" ]; then
  WIKI_COUNT=$(find "$WIKI_DIR" -name "*.md" -type f | wc -l)
  if [ "$WIKI_COUNT" -ge 6 ]; then
    pass "R18.4: centaurion-wiki has $WIKI_COUNT pages (≥6 required)"
  else
    fail "R18.4: centaurion-wiki has $WIKI_COUNT pages (need ≥6)"
  fi
else
  fail "R18.4: docs/centaurion-wiki/ not found"
fi

# R18.5: ROADMAP.md has Phase 1 and Phase 2 marked complete
check_file_contains ".planning/ROADMAP.md" "COMPLETE\|✅" \
  "R18.5: ROADMAP.md has completed phases marked"

# ============================================================
# Summary
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  PHASE 3 RESULTS: $PASS passed, $FAIL failed ($TOTAL total)"
echo "════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "  ✓ ALL PHASE 3 REQUIREMENTS PASS"
  exit 0
else
  echo "  ✗ $FAIL PHASE 3 REQUIREMENT(S) PENDING"
  exit 1
fi
