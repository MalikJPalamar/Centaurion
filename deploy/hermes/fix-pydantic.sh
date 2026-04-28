#!/usr/bin/env bash
# Fix Hermes pydantic / pydantic-core version mismatch.
# Symptom: "SystemError: The installed pydantic-core version (X) is incompatible
#           with the current pydantic version, which requires Y."
#
# Usage (on the Hermes VPS):
#   cd ~/Centaurion && git pull && bash deploy/hermes/fix-pydantic.sh

set -uo pipefail

VENV="${HERMES_VENV:-$HOME/.hermes/hermes-agent/venv}"
PY="$VENV/bin/python"

echo "═══ Hermes pydantic repair ═══"
echo "Venv: $VENV"

if [ ! -x "$PY" ]; then
  echo "✗ Python not found at $PY"
  echo "  Set HERMES_VENV to your venv root, e.g.:"
  echo "    HERMES_VENV=/path/to/venv bash deploy/hermes/fix-pydantic.sh"
  exit 1
fi

echo "▸ Current versions:"
"$PY" -m pip show pydantic pydantic-core 2>/dev/null | grep -E '^(Name|Version):' || true
echo ""

echo "▸ Reinstalling pydantic + pydantic-core (forced, matched pair)..."
"$PY" -m pip install --upgrade --force-reinstall --no-cache-dir pydantic pydantic-core

echo ""
echo "▸ Post-fix versions:"
"$PY" -m pip show pydantic pydantic-core 2>/dev/null | grep -E '^(Name|Version):' || true

echo ""
echo "▸ Smoke test (import pydantic):"
if "$PY" -c "import pydantic; print('  ✓ pydantic', pydantic.VERSION, 'loads cleanly')"; then
  echo ""
  echo "✓ Done. Try: hermes"
else
  echo ""
  echo "✗ Import still failing. Try a clean wipe:"
  echo "    $PY -m pip uninstall -y pydantic pydantic-core"
  echo "    $PY -m pip install pydantic"
  exit 2
fi
