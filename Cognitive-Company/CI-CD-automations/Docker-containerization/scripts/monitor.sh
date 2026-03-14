#!/bin/bash
# Centaurion Status Monitor
# Usage: ./monitor.sh [interval-seconds]

INTERVAL="${1:-60}"
URL="${2:-http://localhost:8000}"

echo "=========================================="
echo "  Centaurion Status Monitor"
echo "  Checking every ${INTERVAL}s"
echo "  Press Ctrl+C to stop"
echo "=========================================="

check_status() {
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

  # Check endpoint
  if curl -s -f "$URL" > /dev/null 2>&1; then
    echo "[$TIMESTAMP] ✅ Healthy"
  else
    echo "[$TIMESTAMP] ❌ Unreachable"
  fi

  # Check container stats if available
  if command -v docker &> /dev/null && docker ps | grep -q centaurion; then
    CPU=$(docker stats --no-stream --format "{{.CPUPerc}}" centaurion 2>/dev/null || echo "N/A")
    MEM=$(docker stats --no-stream --format "{{.MemUsage}}" centaurion 2>/dev/null || echo "N/A")
    echo "   📊 CPU: $CPU | MEM: $MEM"
  fi
}

while true; do
  check_status
  sleep "$INTERVAL"
done
