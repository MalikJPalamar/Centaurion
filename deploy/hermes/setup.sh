#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion → Hermes Integration Setup
# ═══════════════════════════════════════════════════════════
#
# Deploys Centaurion's identity and skills to an existing Hermes installation.
# Run on VPS2 where Hermes is already installed.
#
# Usage:
#   cd ~/Centaurion && bash deploy/hermes/setup.sh
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$(pwd)}"
HERMES_DIR="${HERMES_DIR:-$HOME/.hermes}"

echo "═══ Centaurion → Hermes Setup ═══"
echo "Repo:   $REPO_DIR"
echo "Hermes: $HERMES_DIR"
echo ""

# ── Step 1: Deploy personality ────────────────────────────
echo "▸ Step 1: SOUL.md (Cortex personality)"
if [ -d "$HERMES_DIR" ]; then
  cp "$REPO_DIR/deploy/hermes/SOUL.md" "$HERMES_DIR/SOUL.md"
  echo "  ✓ Deployed to $HERMES_DIR/SOUL.md"
else
  echo "  ✗ Hermes directory not found at $HERMES_DIR"
  echo "    Set HERMES_DIR to your Hermes config path"
  exit 1
fi

# ── Step 2: Deploy memory ────────────────────────────────
echo "▸ Step 2: MEMORY.md (persistent facts)"
cp "$REPO_DIR/deploy/hermes/MEMORY.md" "$HERMES_DIR/MEMORY.md"
echo "  ✓ Deployed to $HERMES_DIR/MEMORY.md"

# ── Step 3: Deploy skills ────────────────────────────────
echo "▸ Step 3: Skills"
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

# ── Step 4: Deploy framework as readable context ─────────
echo "▸ Step 4: Framework docs (accessible to Hermes)"
CONTEXT_DIR="$HERMES_DIR/context/centaurion"
mkdir -p "$CONTEXT_DIR"
cp "$REPO_DIR"/framework/*.md "$CONTEXT_DIR/" 2>/dev/null || true
cp "$REPO_DIR"/identity/*.md "$CONTEXT_DIR/" 2>/dev/null || true
echo "  ✓ Framework + identity files copied to $CONTEXT_DIR/"

# ── Step 5: Verify Hermes can run ─────────────────────────
echo ""
echo "▸ Step 5: Verification"
if command -v hermes &>/dev/null; then
  echo "  ✓ hermes CLI found"
  # Quick test
  HERMES_VER=$(hermes --version 2>/dev/null || echo "unknown")
  echo "  ✓ Version: $HERMES_VER"
else
  echo "  ⚠ hermes CLI not in PATH"
  echo "    Try: pip install hermes-agent"
fi

echo ""
echo "═══ Setup Complete ═══"
echo ""
echo "Test it:"
echo "  hermes"
echo "  > who are you?"
echo ""
echo "Expected: Cortex identity, Three Laws, three ventures."
echo ""
echo "Enable Telegram gateway:"
echo "  hermes gateway telegram --start"
echo ""
echo "This replaces NanoClaw for multi-platform messaging."
