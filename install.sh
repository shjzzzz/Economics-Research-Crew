#!/usr/bin/env bash
# Cross-platform launcher for macOS and Linux (Windows 11 users can use Install-EconomicsResearchCrew.ps1 or python tools/erc_cli.py).
# Usage:
#   ./install.sh --vault ~/MyVault [--platform auto|claude|agy|codex|all] [--with-hooks] [--with-extras] [--update] [--dry-run]
#   ./install.sh test --vault ~/MyVault
#   ./install.sh sync --vault ~/MyVault [--check]
#   ./install.sh check-ars [--out report.md]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  PY="python3"
elif command -v python >/dev/null 2>&1; then
  PY="python"
else
  echo "Error: python3 (or python) is required on PATH." >&2
  exit 1
fi

case "${1:-}" in
  install|test|sync|check-ars)
    exec "$PY" -X utf8 "$SCRIPT_DIR/tools/erc_cli.py" "$@"
    ;;
  *)
    exec "$PY" -X utf8 "$SCRIPT_DIR/tools/erc_cli.py" install "$@"
    ;;
esac
