#!/bin/bash
# Centaurion Deployment Script
# Usage: ./deploy.sh [local|render]

set -e

MODE="${1:-local}"
PORT="${PORT:-8000}"

echo "=========================================="
echo "  Centaurion Deployment Script"
echo "=========================================="
echo "Mode: $MODE"
echo "Port: $PORT"
echo "=========================================="

case "$MODE" in
  local)
    echo "[1/4] Building Docker image..."
    docker build -t centaurion .

    echo "[2/4] Stopping existing container..."
    docker rm -f centaurion 2>/dev/null || true

    echo "[3/4] Starting new container..."
    docker run -d -p $PORT:8000 --name centaurion \
      -e PORT=$PORT \
      -e API_KEYS="${API_KEYS:-}" \
      centaurion

    echo "[4/4] Checking status..."
    sleep 2
    if curl -s http://localhost:$PORT > /dev/null; then
      echo "✅ Deployment successful!"
      echo "🌐 Access at: http://localhost:$PORT"
    else
      echo "❌ Deployment failed - container may be starting up"
      echo "Check with: docker logs centaurion"
    fi
    ;;

  render)
    echo "[1/3] Pushing to GitHub..."
    git add -A
    git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M')" || echo "No changes to commit"
    git push origin main

    echo "[2/3] Triggering Render deployment..."
    echo "✅ GitHub push complete - Render will auto-deploy"

    echo "[3/3] Waiting for deployment..."
    echo "Check status at: https://dashboard.render.com"
    ;;

  *)
    echo "Usage: $0 [local|render]"
    echo "  local  - Deploy to local Docker"
    echo "  render - Push to GitHub (auto-deploys to Render)"
    exit 1
    ;;
esac

echo "=========================================="
