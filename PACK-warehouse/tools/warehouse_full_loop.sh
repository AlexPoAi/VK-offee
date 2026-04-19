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

# Папка Google Drive «Новое» — куда Жанна кладёт файлы
WAREHOUSE_DRIVE_FOLDER_ID="${WAREHOUSE_DRIVE_FOLDER_ID:-1LcTqSJ7n8bl70Ifk0crcL2dYKp3qhL92}"
# Папка Google Drive «Обработано» — куда перемещаем после обработки
WAREHOUSE_DRIVE_PROCESSED_FOLDER_ID="${WAREHOUSE_DRIVE_PROCESSED_FOLDER_ID:-1pHugGbDKpyXqAvGjULiNIMOl64vCc29V}"

{
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop start =========="
  # Синк папки «Новое» Жанны (ABC-анализ, остатки, заявки)
  echo "[warehouse] syncing Zhanna 'Новое' folder: $WAREHOUSE_DRIVE_FOLDER_ID"
  GOOGLE_DRIVE_FOLDER_ID="$WAREHOUSE_DRIVE_FOLDER_ID" "$PYTHON_BIN" "$SCRIPTS_DIR/sync-google-sheets.py"
  # Pipeline: создать карточки + отправить Telegram-отчёт (только если есть новые)
  if [[ -f "$PIPELINE_SCRIPT" ]]; then
    "$PYTHON_BIN" "$PIPELINE_SCRIPT" \
      --hours "$PIPELINE_HOURS" \
      --send-telegram \
      --manual-run
  else
    echo "[warehouse] pipeline script not found: $PIPELINE_SCRIPT"
  fi
  # Переместить обработанные файлы из «Новое» в «Обработано»
  echo "[warehouse] moving processed files to 'Обработано'..."
  "$PYTHON_BIN" -c "
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds_path = Path('$SCRIPTS_DIR/token.pickle')
with open(creds_path, 'rb') as f:
    creds = pickle.load(f)
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
drive = build('drive', 'v3', credentials=creds)

src = '$WAREHOUSE_DRIVE_FOLDER_ID'
dst = '$WAREHOUSE_DRIVE_PROCESSED_FOLDER_ID'
files = drive.files().list(
    q=f\"'{src}' in parents and mimeType!='application/vnd.google-apps.folder' and trashed=false\",
    fields='files(id, name)'
).execute().get('files', [])
for f in files:
    try:
        drive.files().update(fileId=f['id'], addParents=dst, removeParents=src, fields='id').execute()
        print(f'  moved: {f[\"name\"]}')
    except Exception as e:
        # Не валим весь цикл из-за проблем со scope/правами у токена.
        print(f'  move_failed: {f[\"name\"]} :: {e}')
if not files:
    print('  nothing to move')
"
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop done =========="
} >>"$LOG_FILE" 2>>"$ERR_FILE"
