#!/usr/bin/env bash
set -uo pipefail

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
# По умолчанию автоцикл НЕ отправляет Telegram (только обработка/архивация).
# Для принудительной авто-отправки: WAREHOUSE_TELEGRAM_AUTOSEND=1
WAREHOUSE_TELEGRAM_AUTOSEND="${WAREHOUSE_TELEGRAM_AUTOSEND:-0}"

# Папка Google Drive intake — куда Жанна кладёт новые файлы
# Рабочая ветка: root `Отчёты для бота` -> intake `Новые документы`.
# Для sync берём весь root, иначе `ABC`/история в `Обработано` не попадают в локальный контур.
WAREHOUSE_DRIVE_FOLDER_ID="${WAREHOUSE_DRIVE_FOLDER_ID:-1I_aWEHvGVI5c-aAEM03erNZj7HGXtJPf}"
# Intake-папка Жанны — только для последующего move-step.
WAREHOUSE_DRIVE_INTAKE_FOLDER_ID="${WAREHOUSE_DRIVE_INTAKE_FOLDER_ID:-1Jg1Zgj2_ueTV6-NQamAU8XCPalFNhO8W}"
# Папка Google Drive «Обработано» — куда перемещаем после обработки
WAREHOUSE_DRIVE_PROCESSED_FOLDER_ID="${WAREHOUSE_DRIVE_PROCESSED_FOLDER_ID:-1WanukzWeuqJgUQ7N8YkG9oC23-DIRGjT}"

{
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop start =========="
  sync_ok=0
  pipeline_ok=0
  # Синк всего root-контура склада, чтобы видеть и intake, и уже перемещённые
  # в `Обработано` файлы вроде ABC/накладных.
  echo "[warehouse] syncing warehouse root folder: $WAREHOUSE_DRIVE_FOLDER_ID"
  if GOOGLE_DRIVE_FOLDER_ID="$WAREHOUSE_DRIVE_FOLDER_ID" "$PYTHON_BIN" "$SCRIPTS_DIR/sync-google-sheets.py"; then
    sync_ok=1
    echo "[warehouse] sync status=ok"
  else
    echo "[warehouse] sync status=failed (continue with safeguards)"
  fi
  # Pipeline: создать карточки (Telegram по умолчанию выключен в автоцикле)
  if [[ -f "$PIPELINE_SCRIPT" ]]; then
    PIPELINE_ARGS=(--hours "$PIPELINE_HOURS")
    if [[ "$WAREHOUSE_TELEGRAM_AUTOSEND" == "1" ]]; then
      PIPELINE_ARGS+=(--send-telegram)
    fi
    if "$PYTHON_BIN" "$PIPELINE_SCRIPT" "${PIPELINE_ARGS[@]}"; then
      pipeline_ok=1
      echo "[warehouse] pipeline status=ok"
    else
      echo "[warehouse] pipeline status=failed"
    fi
  else
    echo "[warehouse] pipeline script not found: $PIPELINE_SCRIPT"
  fi
  # Переместить обработанные файлы из intake-папки в «Обработано»
  if [[ "$sync_ok" == "1" ]]; then
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

src = '$WAREHOUSE_DRIVE_INTAKE_FOLDER_ID'
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
  else
    echo "[warehouse] move step skipped: sync failed, preventing unsafe moves"
  fi
  if [[ "$sync_ok" == "1" && "$pipeline_ok" == "1" ]]; then
    echo "[warehouse] verdict=ok"
  else
    echo "[warehouse] verdict=warning sync_ok=$sync_ok pipeline_ok=$pipeline_ok"
  fi
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') warehouse_full_loop done =========="
} >>"$LOG_FILE" 2>>"$ERR_FILE"
