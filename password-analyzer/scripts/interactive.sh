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

"$PYTHON_BIN" main.py interactive
