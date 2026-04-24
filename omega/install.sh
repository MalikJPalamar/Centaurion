#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# OMEGA Installer — Centaurion + Hermes + Browser-Harness
# ═══════════════════════════════════════════════════════════
#
# Deploys the Omega stack: Centaurion's identity layer on top of
# Hermes's self-improving engine with browser-harness automation.
#
# Prerequisites:
#   - Hermes installed (`pip install hermes-agent` or from source)
#   - Python 3.11+
#   - Centaurion repo cloned
#
# Usage:
#   cd ~/Centaurion && bash omega/install.sh
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$(pwd)}"
HERMES_DIR="${HERMES_DIR:-$HOME/.hermes}"
BH_REPO="https://github.com/MalikJPalamar/browser-harness.git"
BH_DIR="${BROWSER_HARNESS_DIR:-$HOME/browser-harness}"

echo "═══════════════════════════════════════════════════"
echo "  OMEGA Installer — Centaurion × Hermes × Browser"
echo "═══════════════════════════════════════════════════"
echo ""

# ── Step 1: Verify Hermes ─────────────────────────────────
echo "▸ Step 1: Hermes Engine"
if command -v hermes &>/dev/null; then
  HERMES_VER=$(hermes --version 2>/dev/null || echo "installed")
  echo "  ✓ Hermes found ($HERMES_VER)"
else
  echo "  ✗ Hermes not found."
  echo "    Install: pip install hermes-agent"
  echo "    Or: git clone https://github.com/NousResearch/hermes-agent.git && cd hermes-agent && pip install -e ."
  exit 1
fi

if [ ! -d "$HERMES_DIR" ]; then
  mkdir -p "$HERMES_DIR"
  echo "  Created $HERMES_DIR"
fi
echo ""

# ── Step 2: Deploy Cortex Identity ────────────────────────
echo "▸ Step 2: Cortex Identity (SOUL.md + MEMORY.md)"
cp "$REPO_DIR/omega/SOUL.md" "$HERMES_DIR/SOUL.md"
echo "  ✓ SOUL.md → $HERMES_DIR/SOUL.md"

if [ -f "$REPO_DIR/omega/MEMORY.md" ]; then
  cp "$REPO_DIR/omega/MEMORY.md" "$HERMES_DIR/MEMORY.md"
else
  cp "$REPO_DIR/deploy/hermes/MEMORY.md" "$HERMES_DIR/MEMORY.md"
fi
echo "  ✓ MEMORY.md → $HERMES_DIR/MEMORY.md"

# USER.md for Malik profile
cat > "$HERMES_DIR/USER.md" << 'USERMD'
# Malik Palamar

Three ventures: AOB (Art of Breath), BuilderBee (AI automation), Centaurion.me (framework).
Reviews from phone. Thinks in systems and metaphors. Visual-spatial learner.
Prefers: concise, structured, tradeoffs shown, phone-readable.
USERMD
echo "  ✓ USER.md → $HERMES_DIR/USER.md"
echo ""

# ── Step 3: Deploy Extensions ────────────────────────────
echo "▸ Step 3: Omega Extensions"
EXT_DIR="$HERMES_DIR/extensions"
mkdir -p "$EXT_DIR"

for ext in centaurion_core routing_gate memory_bridge venture_tagger dev_loop; do
  if [ -f "$REPO_DIR/omega/extensions/${ext}.py" ]; then
    cp "$REPO_DIR/omega/extensions/${ext}.py" "$EXT_DIR/${ext}.py"
    echo "  ✓ ${ext}.py"
  fi
done
echo ""

# ── Step 4: Deploy Skills ────────────────────────────────
echo "▸ Step 4: Centaurion Skills"
SKILLS_DIR="$HERMES_DIR/skills"
mkdir -p "$SKILLS_DIR"

for skill_dir in "$REPO_DIR"/skills/*/; do
  SKILL_NAME=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    mkdir -p "$SKILLS_DIR/$SKILL_NAME"
    cp "$skill_dir/SKILL.md" "$SKILLS_DIR/$SKILL_NAME/SKILL.md"
    echo "  ✓ $SKILL_NAME"
  fi
done
echo ""

# ── Step 5: Deploy Tools ──────────────────────────────────
echo "▸ Step 5: Omega Tools"
TOOLS_DIR="$HERMES_DIR/tools"
mkdir -p "$TOOLS_DIR"

for tool in browser_harness wiki_manager; do
  if [ -f "$REPO_DIR/omega/tools/${tool}.py" ]; then
    cp "$REPO_DIR/omega/tools/${tool}.py" "$TOOLS_DIR/${tool}.py"
    echo "  ✓ ${tool}.py"
  fi
done

if [ -d "$BH_DIR/.git" ]; then
  echo "  ✓ browser-harness already cloned at $BH_DIR"
else
  echo "  Cloning browser-harness..."
  git clone "$BH_REPO" "$BH_DIR" 2>&1 | tail -1 || echo "  ⚠ Clone failed"
fi

if [ -d "$BH_DIR" ] && command -v pip3 &>/dev/null; then
  pip3 install -e "$BH_DIR" 2>&1 | tail -1 || echo "  ⚠ pip install failed"
  echo "  ✓ browser-harness dependencies installed"
fi
echo ""

# ── Step 6: Set Environment ──────────────────────────────
echo "▸ Step 6: Environment"
ENVFILE="$HERMES_DIR/.env"
if [ ! -f "$ENVFILE" ]; then
  cat > "$ENVFILE" << 'ENVEOF'
# Omega Environment
CENTAURION_REPO=$HOME/Centaurion
BROWSER_HARNESS_DIR=$HOME/browser-harness
ENVEOF
  echo "  ✓ Created $ENVFILE"
else
  echo "  ✓ $ENVFILE already exists"
fi
echo ""

# ── Step 7: Verify ────────────────────────────────────────
echo "▸ Step 7: Verification"
echo "  Checking deployed files..."

CHECKS=0
PASS=0
for f in SOUL.md MEMORY.md USER.md; do
  CHECKS=$((CHECKS + 1))
  if [ -f "$HERMES_DIR/$f" ]; then
    PASS=$((PASS + 1))
    echo "    ✓ $f"
  else
    echo "    ✗ $f missing"
  fi
done

for f in centaurion_core.py routing_gate.py; do
  CHECKS=$((CHECKS + 1))
  if [ -f "$EXT_DIR/$f" ]; then
    PASS=$((PASS + 1))
    echo "    ✓ extensions/$f"
  else
    echo "    ✗ extensions/$f missing"
  fi
done

SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" -type f 2>/dev/null | wc -l)
echo "    ✓ $SKILL_COUNT skills deployed"

echo ""
echo "═══════════════════════════════════════════════════"
echo "  OMEGA Installed ($PASS/$CHECKS core files)"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  Test it:"
echo "    hermes"
echo "    > who are you?"
echo ""
echo "  Expected: Cortex identity, Three Laws, three ventures."
echo ""
echo "  Enable Telegram:"
echo "    hermes gateway telegram --start"
echo ""
echo "  Browser automation:"
echo "    hermes"
echo "    > navigate to github.com/MalikJPalamar/Centaurion and screenshot"
echo ""
