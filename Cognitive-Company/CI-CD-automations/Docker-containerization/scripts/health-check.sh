#!/bin/bash
# Centaurion Health Check Script
# Usage: ./health-check.sh [url]

URL="${1:-http://localhost:8000}"

echo "=========================================="
echo "  Centaurion Health Check"
echo "=========================================="

# Check main endpoint
echo "Checking main endpoint..."
if curl -s -f "$URL" > /dev/null; then
  echo "✅ Main endpoint: OK"
else
  echo "❌ Main endpoint: FAILED"
fi

# Check status endpoint
echo "Checking status endpoint..."
STATUS_RESPONSE=$(curl -s "$URL/status" 2>/dev/null)
if echo "$STATUS_RESPONSE" | grep -q "running"; then
  echo "✅ Status endpoint: OK"
  echo "   Response: $STATUS_RESPONSE"
else
  echo "❌ Status endpoint: FAILED"
fi

# Check container (if running locally)
if command -v docker &> /dev/null; then
  echo "Checking Docker container..."
  if docker ps | grep -q centaurion; then
    echo "✅ Container: Running"
    docker stats --no-stream centaurion 2>/dev/null | tail -1 || true
  else
    echo "⚠️  Container: Not running"
  fi
fi

echo "=========================================="
