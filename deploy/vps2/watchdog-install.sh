#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# Routing Watchdog — Installer
# ═══════════════════════════════════════════════════════════
#
# Installs the watchdog as a systemd service.
# Hermes runs as user process. Watchdog runs as system service.
# Hermes CANNOT stop, modify, or disable the watchdog.
#
# Usage:
#   sudo bash deploy/vps2/watchdog-install.sh
#
# ═══════════════════════════════════════════════════════════

set -uo pipefail

CENTAURION_REPO="${CENTAURION_REPO:-$HOME/Centaurion}"
WATCHDOG_SCRIPT="$CENTAURION_REPO/deploy/vps2/routing-watchdog.sh"
SERVICE_NAME="centaurion-watchdog"

echo "═══ Routing Watchdog Installer ═══"

# ── Step 1: Verify watchdog script exists ─────────────────
if [ ! -f "$WATCHDOG_SCRIPT" ]; then
  echo "✗ Watchdog script not found: $WATCHDOG_SCRIPT"
  exit 1
fi
chmod +x "$WATCHDOG_SCRIPT"
echo "✓ Watchdog script: $WATCHDOG_SCRIPT"

# ── Step 2: Create systemd service ───────────────────────
cat > /etc/systemd/system/${SERVICE_NAME}.service << UNIT
[Unit]
Description=Centaurion Routing Gate Watchdog
Documentation=https://github.com/MalikJPalamar/Centaurion
After=network.target
# Start after Hermes gateway if it exists
After=hermes-gateway.service

[Service]
Type=simple
ExecStart=/bin/bash $WATCHDOG_SCRIPT
Restart=always
RestartSec=10
Environment=CENTAURION_REPO=$CENTAURION_REPO
Environment=WATCHDOG_INTERVAL=30

# Telegram alerts (configure these)
# Environment=TELEGRAM_BOT_TOKEN=your-bot-token
# Environment=TELEGRAM_CHAT_ID=your-chat-id

# Security: run as root so Hermes (user process) cannot kill it
User=root
Group=root

# Watchdog cannot be stopped by non-root
ProtectSystem=false
ProtectHome=false

[Install]
WantedBy=multi-user.target
UNIT

echo "✓ Systemd service created: ${SERVICE_NAME}.service"

# ── Step 3: Enable and start ─────────────────────────────
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl start ${SERVICE_NAME}

echo "✓ Service enabled and started"

# ── Step 4: Verify ───────────────────────────────────────
sleep 2
STATUS=$(systemctl is-active ${SERVICE_NAME})
echo ""
echo "Service status: $STATUS"
echo ""

if [ "$STATUS" = "active" ]; then
  echo "═══ Watchdog Installed ═══"
  echo ""
  echo "  Status:    systemctl status $SERVICE_NAME"
  echo "  Logs:      journalctl -u $SERVICE_NAME -f"
  echo "  Alerts:    cat $CENTAURION_REPO/memory/state/watchdog-alerts.jsonl"
  echo "  Stop:      systemctl stop $SERVICE_NAME (requires root)"
  echo ""
  echo "  Hermes CANNOT disable this service."
  echo "  Only root can stop it: systemctl stop $SERVICE_NAME"
  echo ""
  echo "  To add Telegram alerts, edit:"
  echo "    /etc/systemd/system/${SERVICE_NAME}.service"
  echo "  Uncomment TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID lines."
  echo "  Then: systemctl daemon-reload && systemctl restart $SERVICE_NAME"
else
  echo "⚠ Service not active. Check: journalctl -u $SERVICE_NAME -n 20"
fi
