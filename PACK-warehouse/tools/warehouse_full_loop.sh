#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS_DIR="$ROOT_DIR/.github/scripts"
LOG_FILE="$SCRIPTS_DIR/sync.log"
ERR_FILE="$SCRIPTS_DIR/sync.error.log"

mkdir -p "$SCRIPTS_DIR"

if [[ -x "$SCRIPTS_DIR/venv/bin/python3" ]]; then
  PYTHON_BIN="$SCRIPTS_DIR/venv/bin/python3"
else
  PYTHON_BIN="python3"
fi

{
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop start =========="
  "$PYTHON_BIN" "$SCRIPTS_DIR/sync-google-sheets.py"
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop done =========="
} >>"$LOG_FILE" 2>>"$ERR_FILE"
