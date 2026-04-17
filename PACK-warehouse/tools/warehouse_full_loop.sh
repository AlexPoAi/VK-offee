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

PIPELINE_SCRIPT="$ROOT_DIR/PACK-warehouse/tools/warehouse_reports_pipeline.py"
PIPELINE_HOURS="${WAREHOUSE_PIPELINE_HOURS:-336}"
MANUAL_REPORT=0

# Папка Google Drive с отчётами склада (Жанна: ABC-анализ, остатки, заявки)
WAREHOUSE_DRIVE_FOLDER_ID="${WAREHOUSE_DRIVE_FOLDER_ID:-1oo1j86l7hGZ-E1HIbAApc3PdCA3o80GX}"

if [[ "${1:-}" == "--manual-report" ]]; then
  MANUAL_REPORT=1
fi

{
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop start =========="
  # Синк общей папки кофейни
  "$PYTHON_BIN" "$SCRIPTS_DIR/sync-google-sheets.py"
  # Синк папки склада Жанны (ABC-анализ, остатки, заявки)
  echo "[warehouse] syncing Zhanna reports folder: $WAREHOUSE_DRIVE_FOLDER_ID"
  GOOGLE_DRIVE_FOLDER_ID="$WAREHOUSE_DRIVE_FOLDER_ID" "$PYTHON_BIN" "$SCRIPTS_DIR/sync-google-sheets.py"
  if [[ -f "$PIPELINE_SCRIPT" ]]; then
    if [[ "$MANUAL_REPORT" -eq 1 ]]; then
      "$PYTHON_BIN" "$PIPELINE_SCRIPT" \
        --hours "$PIPELINE_HOURS" \
        --send-telegram \
        --manual-run \
        --telegram-on-empty
    else
      "$PYTHON_BIN" "$PIPELINE_SCRIPT" --hours "$PIPELINE_HOURS" --send-telegram
    fi
  else
    echo "[warehouse] pipeline script not found: $PIPELINE_SCRIPT"
  fi
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop done =========="
} >>"$LOG_FILE" 2>>"$ERR_FILE"
