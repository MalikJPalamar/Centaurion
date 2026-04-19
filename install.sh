#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Installer — One-Command VPS Setup
# ═══════════════════════════════════════════════════════════
#
# Sets up the complete Centaurion exo-cortex on a VPS:
#   - Clones repo (or pulls latest)
#   - Verifies Claude Code auth
#   - Installs cron jobs (dev loop 3x daily, weekly review, health check)
#   - Deploys Nova SOUL.md to NanoClaw (if present)
#   - Runs health check
#   - Runs test suite
#
# Usage:
#   curl -sL https://raw.githubusercontent.com/MalikJPalamar/Centaurion/main/install.sh | bash
#   # or from the repo:
#   bash install.sh
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_URL="https://github.com/MalikJPalamar/Centaurion.git"
REPO_DIR="${CENTAURION_REPO:-$HOME/Centaurion}"
LOG_DIR="$REPO_DIR/logs"

echo "═══════════════════════════════════════════════════"
echo "  Centaurion Installer"
echo "═══════════════════════════════════════════════════"
echo ""

# ── Step 1: Clone or pull repo ────────────────────────────
echo "▸ Step 1: Repository"
if [ -d "$REPO_DIR/.git" ]; then
  echo "  Repo exists at $REPO_DIR — pulling latest..."
  cd "$REPO_DIR"
  git pull origin main 2>&1 | tail -1
else
  echo "  Cloning to $REPO_DIR..."
  git clone "$REPO_URL" "$REPO_DIR" 2>&1 | tail -1
  cd "$REPO_DIR"
fi
echo "  ✓ Repository ready"
echo ""

# ── Step 2: Verify Claude Code ────────────────────────────
echo "▸ Step 2: Claude Code Authentication"
if command -v claude &>/dev/null; then
  AUTH=$(claude auth status 2>/dev/null | grep -o '"authMethod": *"[^"]*"' | sed 's/.*: *"//;s/"//' || echo "unknown")
  if [ "$AUTH" = "claude.ai" ] || [ "$AUTH" = "oauth_token" ]; then
    echo "  ✓ Authenticated via $AUTH (Max subscription)"
  elif [ "$AUTH" = "none" ]; then
    echo "  ✗ Not authenticated. Run: claude auth login"
    echo "    Then re-run this installer."
    exit 1
  else
    echo "  ⚠ Auth method: $AUTH (may incur API charges)"
  fi
else
  echo "  ✗ Claude Code CLI not found."
  echo "    Install: npm install -g @anthropic-ai/claude-code"
  exit 1
fi
echo ""

# ── Step 3: Create directories ────────────────────────────
echo "▸ Step 3: Directories"
mkdir -p "$LOG_DIR" "$REPO_DIR/memory/state"
echo "  ✓ logs/ and memory/state/ ready"
echo ""

# ── Step 4: Install cron jobs ─────────────────────────────
echo "▸ Step 4: Cron Jobs"
CRON_BASE="cd $REPO_DIR && CENTAURION_REPO=$REPO_DIR bash"
EXISTING=$(crontab -l 2>/dev/null || true)

NEEDS_INSTALL=false
if ! echo "$EXISTING" | grep -q "centaurion-dev-loop"; then
  NEEDS_INSTALL=true
fi

if [ "$NEEDS_INSTALL" = true ]; then
  (echo "$EXISTING"
   echo "# Centaurion Dev Loop — 3x daily (6am, 2pm, 10pm CET)"
   echo "0 4 * * * $CRON_BASE deploy/vps1/centaurion-dev-loop.sh >> $LOG_DIR/cron.log 2>&1"
   echo "0 12 * * * $CRON_BASE deploy/vps1/centaurion-dev-loop.sh >> $LOG_DIR/cron.log 2>&1"
   echo "0 20 * * * $CRON_BASE deploy/vps1/centaurion-dev-loop.sh >> $LOG_DIR/cron.log 2>&1"
   echo "# Centaurion Weekly Review — Mondays 7am CET"
   echo "0 5 * * 1 $CRON_BASE deploy/vps1/weekly-review.sh >> $LOG_DIR/cron.log 2>&1"
   echo "# Centaurion Health Check — daily 5:55am CET (before dev loop)"
   echo "55 3 * * * $CRON_BASE deploy/vps1/health-check.sh >> $LOG_DIR/cron.log 2>&1"
   echo "# Centaurion Private Data Sync — nightly 21:00 UTC (idempotent; skips when no changes)"
   echo "0 21 * * * $CRON_BASE deploy/vps1/sync-private.sh >> $LOG_DIR/sync-private.log 2>&1"
  ) | crontab -
  echo "  ✓ Installed:"
  echo "    Dev loop:     6am, 2pm, 10pm CET (3x daily)"
  echo "    Weekly review: Monday 7am CET"
  echo "    Health check:  5:55am CET (daily, before dev loop)"
  echo "    Private sync:  21:00 UTC daily (only commits when changes present)"
else
  echo "  ✓ Cron jobs already installed"
fi
echo ""

# ── Step 5: Deploy Nova to NanoClaw ───────────────────────
echo "▸ Step 5: NanoClaw / Nova"
NANOCLAW_DIR=""
for candidate in /root/nanoclaw "$HOME/nanoclaw"; do
  if [ -d "$candidate" ]; then NANOCLAW_DIR="$candidate"; break; fi
done

if [ -n "$NANOCLAW_DIR" ]; then
  if [ -f "$REPO_DIR/agents/Nova.md" ]; then
    cp "$REPO_DIR/agents/Nova.md" "$NANOCLAW_DIR/SOUL.md"
    echo "  ✓ Nova personality deployed to $NANOCLAW_DIR/SOUL.md"
  else
    echo "  ⚠ agents/Nova.md not found in repo"
  fi

  if docker ps --format '{{.Names}}' 2>/dev/null | grep -qi "nanoclaw\|claw"; then
    echo "  ✓ NanoClaw container is running"
  else
    echo "  ⚠ NanoClaw container not running — start it manually"
  fi
else
  echo "  ⚠ NanoClaw directory not found (skipping)"
fi
echo ""

# ── Step 6: Run health check ─────────────────────────────
echo "▸ Step 6: Health Check"
CENTAURION_REPO="$REPO_DIR" bash "$REPO_DIR/deploy/vps1/health-check.sh" 2>/dev/null | grep -E "Disk:|Memory:|Docker:|NanoClaw:|Claude:|Status:"
echo ""

# ── Step 7: Run test suite ────────────────────────────────
echo "▸ Step 7: Test Suite"
RESULT=$(CENTAURION_REPO="$REPO_DIR" bash "$REPO_DIR/tests/run-all.sh" 2>&1)
echo "$RESULT" | grep -E "✓ Phase|✗ Phase|✓ Infra|✗ Infra|TOTAL"
echo ""

# ── Summary ───────────────────────────────────────────────
echo "═══════════════════════════════════════════════════"
echo "  Centaurion Installed"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  Repo:    $REPO_DIR"
echo "  Auth:    $AUTH"
echo "  Crons:   $(crontab -l 2>/dev/null | grep -c centaurion) jobs"
echo "  Logs:    $LOG_DIR/"
echo ""
echo "  Next steps:"
echo "  1. Test dev loop:   CENTAURION_REPO=$REPO_DIR bash deploy/vps1/centaurion-dev-loop.sh"
echo "  2. Test weekly:     CENTAURION_REPO=$REPO_DIR bash deploy/vps1/weekly-review.sh"
echo "  3. Open in Claude:  cd $REPO_DIR && claude"
echo ""

# ── Onboarding check ──────────────────────────────────────
if [ ! -f "$REPO_DIR/memory/state/onboarding-state.json" ]; then
  echo "  ℹ First-time install detected."
  echo "    When you open Claude Code for the first time, Cortex will run the"
  echo "    AQAL + ILP baseline assessment (Light 25Q / Deep 75Q / Skip) to"
  echo "    calibrate the system to you specifically. This runs ONCE —"
  echo "    never again unless the 90-day refresh is due."
  echo ""
  echo "    Start: cd $REPO_DIR && claude"
  echo ""
fi
