#!/bin/bash
# Centaurion Rollback Script
# Usage: ./rollback.sh [previous-commit-hash]

set -e

COMMIT="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  Centaurion Rollback"
echo "=========================================="

if [ -z "$COMMIT" ]; then
  echo "Finding previous commit..."
  COMMIT=$(git log --oneline -2 | tail -1 | cut -d' ' -f1)
  echo "Rolling back to: $COMMIT"
fi

echo "[1/3] Reverting to commit $COMMIT..."
git checkout "$COMMIT"

echo "[2/3] Rebuilding Docker..."
cd "$SCRIPT_DIR"
docker build -t centaurion .

echo "[3/3] Restarting container..."
docker rm -f centaurion 2>/dev/null || true
docker run -d -p 8000:8000 --name centaurion centaurion

echo "✅ Rollback complete!"
echo "🌐 Check: http://localhost:8000"

echo "=========================================="
