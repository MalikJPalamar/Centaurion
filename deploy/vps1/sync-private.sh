#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Centaurion Private Data Sync
# ═══════════════════════════════════════════════════════════
#
# Mirrors gitignored personal data from the public Centaurion
# checkout to a separate private git repo (default
# MalikJPalamar/centaurion-private, clone path ~/centaurion-private).
#
# Paths are mirrored 1:1 — identity/BASELINE-*.md → identity/,
# memory/state/baseline-*.md → memory/state/, etc.
#
# Usage:
#   bash deploy/vps1/sync-private.sh           # one-shot sync + push
#   PRIVATE_DIR=/path/to/private bash ...       # override location
#
# Safe to schedule via cron after dev loops or weekly review:
#   0 21 * * * cd ~/Centaurion && bash deploy/vps1/sync-private.sh \
#              >> ~/Centaurion/logs/sync-private.log 2>&1
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

REPO_DIR="${CENTAURION_REPO:-$HOME/Centaurion}"
PRIVATE_DIR="${PRIVATE_DIR:-$HOME/centaurion-private}"
DATE=$(date -u +%Y-%m-%dT%H:%MZ)

log() { echo "[$(date '+%H:%M:%S')] $*"; }

# ── Safety checks ─────────────────────────────────────────
if [ ! -d "$REPO_DIR" ]; then
  log "ERROR: public repo not found at $REPO_DIR"
  exit 1
fi

if [ ! -d "$PRIVATE_DIR/.git" ]; then
  log "ERROR: private repo not found at $PRIVATE_DIR"
  log "  Create it first:"
  log "    gh repo create MalikJPalamar/centaurion-private --private"
  log "    git clone git@github.com:MalikJPalamar/centaurion-private.git $PRIVATE_DIR"
  exit 1
fi

cd "$REPO_DIR"

# ── Verify private-repo remote is NOT the public one ─────
PRIVATE_REMOTE=$(cd "$PRIVATE_DIR" && git remote get-url origin 2>/dev/null || echo "")
if echo "$PRIVATE_REMOTE" | grep -q "MalikJPalamar/Centaurion.git"; then
  log "FATAL: private dir points at the PUBLIC repo. Aborting."
  exit 1
fi

log "Public:  $REPO_DIR"
log "Private: $PRIVATE_DIR ($PRIVATE_REMOTE)"

# ── Paths to sync (must match .gitignore private block) ──
declare -a PATHS=(
  "identity/BASELINE-INTEGRAL.md"
  "memory/state/baseline-light-in-progress.md"
  "memory/state/baseline-deep-in-progress.md"
  "memory/state/onboarding-state.json"
  "memory/state/routing-adjustments.jsonl"
  "memory/state/autoresearch-ur-protocol-results.md"
  "memory/state/autoresearch-spof-mitigation-results.md"
)

CHANGES=0
for p in "${PATHS[@]}"; do
  src="$REPO_DIR/$p"
  dest="$PRIVATE_DIR/$p"
  if [ -f "$src" ]; then
    mkdir -p "$(dirname "$dest")"
    if [ ! -f "$dest" ] || ! cmp -s "$src" "$dest"; then
      cp "$src" "$dest"
      log "  synced: $p"
      CHANGES=$((CHANGES+1))
    fi
  fi
done

if [ "$CHANGES" -eq 0 ]; then
  log "No changes. Private repo already current."
  exit 0
fi

# ── Commit + push to PRIVATE remote only ─────────────────
cd "$PRIVATE_DIR"
git add -A
COMMIT_MSG="sync: $CHANGES file(s) from public repo · $DATE"
git -c user.email="malik@builderbee.co" -c user.name="Malik Palamar" \
    commit -q -m "$COMMIT_MSG"
git push -q origin main
log "Pushed $CHANGES change(s) to private repo."
