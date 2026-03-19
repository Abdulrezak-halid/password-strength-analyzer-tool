#!/usr/bin/env bash
set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: Python interpreter not found (python3/python)."
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: ./scripts/quick_check.sh <password> [username]"
  exit 1
fi

PASSWORD="$1"
USERNAME="${2:-}"

if [[ -n "$USERNAME" ]]; then
  "$PYTHON_BIN" main.py check --password "$PASSWORD" --username "$USERNAME"
else
  "$PYTHON_BIN" main.py check --password "$PASSWORD"
fi
