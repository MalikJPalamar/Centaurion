#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Browser-Harness Setup for Centaurion
# ═══════════════════════════════════════════════════════════
#
# Clones and configures browser-harness as a tool for Hermes/Cortex.
# Requires Python 3.11+ and Chrome/Chromium.
#
# Usage:
#   bash deploy/browser-harness/setup.sh
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$(pwd)}"
BH_DIR="${BROWSER_HARNESS_DIR:-$HOME/browser-harness}"
BH_REPO="https://github.com/MalikJPalamar/browser-harness.git"

echo "═══ Browser-Harness Setup ═══"

# ── Step 1: Clone or pull ─────────────────────────────────
echo "▸ Step 1: Repository"
if [ -d "$BH_DIR/.git" ]; then
  echo "  Exists at $BH_DIR — pulling..."
  cd "$BH_DIR" && git pull origin main 2>&1 | tail -1
else
  echo "  Cloning to $BH_DIR..."
  git clone "$BH_REPO" "$BH_DIR" 2>&1 | tail -1
fi
echo "  ✓ Repository ready"

# ── Step 2: Install dependencies ──────────────────────────
echo "▸ Step 2: Dependencies"
cd "$BH_DIR"
if command -v pip &>/dev/null; then
  pip install -e . 2>&1 | tail -3
  echo "  ✓ Python dependencies installed"
else
  echo "  ✗ pip not found — install Python 3.11+"
  exit 1
fi

# ── Step 3: Check Chrome ──────────────────────────────────
echo "▸ Step 3: Chrome/Chromium"
if command -v google-chrome &>/dev/null || command -v chromium-browser &>/dev/null || command -v chromium &>/dev/null; then
  echo "  ✓ Chrome/Chromium found"
else
  echo "  ⚠ Chrome not found. Install:"
  echo "    apt install chromium-browser"
  echo "    # or for headless:"
  echo "    apt install chromium-browser --no-install-recommends"
fi

# ── Step 4: Create Centaurion skill for browser tasks ─────
echo "▸ Step 4: Browser skill"
SKILL_FILE="$BH_DIR/domain-skills/centaurion/SKILL.md"
mkdir -p "$(dirname "$SKILL_FILE")"
cat > "$SKILL_FILE" << 'SKILL'
---
name: centaurion-browser
description: Browser automation for Centaurion ventures. USE WHEN a task requires web interaction — form filling, data extraction, monitoring, screenshots.
---

# Centaurion Browser Skill

## Venture-Specific Patterns

### AOB (Art of Breath)
- Monitor Mighty Networks community metrics
- Check Ontraport/GHL dashboard stats
- Screenshot facilitator certification page for reporting

### BuilderBee
- Audit client GHL sub-accounts
- Test lead capture funnels end-to-end
- Monitor client website uptime and SEO metrics

### Centaurion.me
- Monitor GitHub repo stats (stars, forks, issues)
- Check framework documentation accessibility
- Research competitor positioning

## Routing
Browser tasks are medium-stakes, reversible (read-only by default) → auto-execute.
Write actions (form submissions, account changes) → surface to Malik first.
SKILL

echo "  ✓ Centaurion browser skill created"

echo ""
echo "═══ Setup Complete ═══"
echo ""
echo "Test it:"
echo "  cd $BH_DIR && python run.py"
echo ""
echo "Register as Hermes tool:"
echo "  Copy domain-skills/centaurion/ to ~/.hermes/skills/"
