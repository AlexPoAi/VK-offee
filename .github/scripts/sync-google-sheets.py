#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
АВТОМАТИЧЕСКАЯ синхронизация ВСЕХ Google Sheets из папки Drive
Находит все таблицы автоматически, не нужно добавлять вручную
"""

import os
import sys
import random
import time
import io
from pathlib import Path
import pickle
import csv
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"

# ID папки Google Drive (можно переопределить через env GOOGLE_DRIVE_FOLDER_ID)
DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC')

# Маппинг папок (куда сохранять таблицы)
FOLDER_MAPPING = {
    'БАР': 'БАР',
    'КУХНЯ': 'КУХНЯ',
    'Персонал': 'Персонал',
    'ДЛЯ ШЕФА': 'ДЛЯ ШЕФА',
    'Инвентаризация': 'Инвентаризация',
    'Документы': 'Документы',
    'ПОСТАВЩИКИ': 'ПОСТАВЩИКИ',
}

stats = {'success': 0, 'failed': 0, 'sheets_read': 0, 'tables_found': 0}


def _is_retryable_http_error(exc):
    """Проверяем, стоит ли повторять запрос (quota / transient)."""
    status = getattr(exc, "status_code", None)
    if status is None and getattr(exc, "resp", None) is not None:
        status = getattr(exc.resp, "status", None)
    if status in (429, 500, 502, 503, 504):
        return True
    text = str(exc).lower()
    return ("quota" in text) or ("rate limit" in text) or ("backend error" in text)


def execute_google_request(call, label, max_attempts=5, base_delay=1.5):
    """Выполнить Google API запрос с экспоненциальным backoff."""
    for attempt in range(1, max_attempts + 1):
        try:
            return call.execute()
        except HttpError as exc:
            if (not _is_retryable_http_error(exc)) or (attempt == max_attempts):
                raise
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.6)
            print(f"  ⏳ Retry {attempt}/{max_attempts} [{label}] after {delay:.1f}s ({exc})")
            time.sleep(delay)
        except Exception:
            # Не скрываем неизвестные ошибки.
            raise


def sanitize_filename(name):
    """Безопасное имя файла для macOS/Linux."""
    forbidden = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    safe = name
    for ch in forbidden:
        safe = safe.replace(ch, '-')
    # Схлопываем повторяющиеся пробелы по краям
    return safe.strip()

def get_credentials():
    creds = None
    token_path = Path(__file__).parent / 'token.pickle'

    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = Path(__file__).parent / 'credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def find_all_spreadsheets(drive_service, folder_id):
    """Найти все Google Sheets в папке и подпапках"""
    spreadsheets = []

    def search_folder(folder_id, parent_path=""):
        query = f"'{folder_id}' in parents and trashed=false"
        results = execute_google_request(
            drive_service.files().list(
                q=query,
                fields="files(id, name, mimeType, parents)",
                pageSize=1000
            ),
            label=f"drive.files.list:{parent_path or 'root'}",
        )

        items = results.get('files', [])

        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                # Это Google Sheet
                spreadsheets.append({
                    'id': item['id'],
                    'name': item['name'],
                    'path': parent_path
                })
                stats['tables_found'] += 1

            elif item['mimeType'] == 'application/vnd.google-apps.folder':
                # Это папка, рекурсивно ищем внутри
                folder_name = item['name']
                new_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
                search_folder(item['id'], new_path)

    search_folder(folder_id)
    return spreadsheets


def find_supported_files(drive_service, folder_id):
    """
    Найти поддерживаемые non-GoogleSheet файлы в папке и подпапках.
    Сейчас поддерживаем:
      - text/csv
      - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (.xlsx)
      - application/pdf (.pdf)
    """
    files = []
    supported_mimes = {
        'text/csv',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/pdf',
    }

    def search_folder(current_folder_id, parent_path=""):
        query = f"'{current_folder_id}' in parents and trashed=false"
        results = execute_google_request(
            drive_service.files().list(
                q=query,
                fields="files(id, name, mimeType, parents)",
                pageSize=1000
            ),
            label=f"drive.files.list:files:{parent_path or 'root'}",
        )

        items = results.get('files', [])
        for item in items:
            mime = item.get('mimeType')
            if mime == 'application/vnd.google-apps.folder':
                folder_name = item['name']
                new_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
                search_folder(item['id'], new_path)
                continue

            if mime in supported_mimes:
                files.append({
                    'id': item['id'],
                    'name': item['name'],
                    'path': parent_path,
                    'mimeType': mime,
                })

    search_folder(folder_id)
    return files


def download_drive_file_bytes(drive_service, file_id):
    """Скачать файл из Google Drive в память."""
    request = drive_service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()

def get_sheet_names(sheets_service, sheet_id):
    """Получить названия всех листов в таблице"""
    try:
        sheet_metadata = execute_google_request(
            sheets_service.spreadsheets().get(spreadsheetId=sheet_id),
            label=f"sheets.spreadsheets.get:{sheet_id}",
        )
        sheets = sheet_metadata.get('sheets', [])
        return [sheet['properties']['title'] for sheet in sheets]
    except Exception as e:
        print(f"  ❌ Ошибка получения листов: {e}")
        return []

def read_sheet_data(sheets_service, sheet_id, sheet_name):
    """Чтение данных из конкретного листа"""
    try:
        result = execute_google_request(
            sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=f"'{sheet_name}'"
            ),
            label=f"sheets.values.get:{sheet_id}:{sheet_name}",
        )

        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"    ❌ Ошибка чтения листа '{sheet_name}': {e}")
        return None

def save_as_csv(data, file_path):
    """Сохранение данных в CSV"""
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def save_csv_bytes(raw_bytes, file_path):
    """Сохранение CSV-байтов с мягкой декодировкой."""
    text = None
    for enc in ('utf-8-sig', 'utf-8', 'cp1251'):
        try:
            text = raw_bytes.decode(enc)
            break
        except Exception:
            continue
    if text is None:
        text = raw_bytes.decode('utf-8', errors='replace')
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def save_binary_bytes(raw_bytes, file_path):
    file_path.write_bytes(raw_bytes)


def save_xlsx_bytes_as_csvs(raw_bytes, folder_path, base_name):
    """Конвертировать XLSX в CSV по листам. Возвращает количество созданных CSV."""
    try:
        import openpyxl  # optional runtime dependency
    except Exception as e:
        print(f"  ⚠️ openpyxl недоступен, XLSX пропущен: {e}")
        return 0

    created = 0
    wb = openpyxl.load_workbook(io.BytesIO(raw_bytes), data_only=True, read_only=True)
    for ws in wb.worksheets:
        safe_sheet = sanitize_filename(ws.title)
        out = folder_path / f"{base_name} - {safe_sheet}.csv"
        with open(out, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for row in ws.iter_rows(values_only=True):
                writer.writerow(["" if v is None else v for v in row])
        created += 1
    return created

def determine_folder(table_path):
    """Определить папку для сохранения на основе пути"""
    for key, value in FOLDER_MAPPING.items():
        if key in table_path:
            return value
    return "Разное"  # По умолчанию

def main():
    print("="*70)
    print("🔄 АВТОМАТИЧЕСКАЯ СИНХРОНИЗАЦИЯ ВСЕХ GOOGLE SHEETS")
    print("="*70)
    print()

    # Авторизация
    print("🔑 Авторизация...")
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    print("✅ Авторизация успешна")
    print()

    # Поиск всех Google Sheets
    print(f"🔍 Поиск Google Sheets в папке {DRIVE_FOLDER_ID}...")
    spreadsheets = find_all_spreadsheets(drive_service, DRIVE_FOLDER_ID)
    print(f"✅ Найдено таблиц: {len(spreadsheets)}")
    print()

    # Синхронизация каждой таблицы
    for table in spreadsheets:
        sheet_id = table['id']
        table_name = table['name']
        table_path = table['path']

        print(f"📊 {table_name} ({table_path})")

        # Определить папку для сохранения
        save_folder = determine_folder(table_path)
        folder_path = KNOWLEDGE_BASE_PATH / save_folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Получить все листы
        sheet_names = get_sheet_names(sheets_service, sheet_id)

        if not sheet_names:
            print(f"  ❌ Не удалось получить листы")
            stats['failed'] += 1
            continue

        print(f"  📄 Найдено листов: {len(sheet_names)}")

        # Читать каждый лист
        for sheet_name in sheet_names:
            print(f"    📥 {sheet_name}...", end=" ")

            data = read_sheet_data(sheets_service, sheet_id, sheet_name)

            if data is None:
                stats['failed'] += 1
                continue

            if not data:
                print("⚠️  Пустой")
                continue

            # Сохранить CSV
            safe_table_name = sanitize_filename(table_name)
            safe_name = sanitize_filename(sheet_name)
            file_path = folder_path / f"{safe_table_name} - {safe_name}.csv"
            save_as_csv(data, file_path)

            print(f"✅ ({len(data)} строк)")
            stats['sheets_read'] += 1

        stats['success'] += 1
        print()

    # Дополнительно: синк поддерживаемых файлов (CSV/XLSX), загруженных как файлы
    print("📎 Поиск загруженных CSV/XLSX файлов...")
    extra_files = find_supported_files(drive_service, DRIVE_FOLDER_ID)
    print(f"✅ Найдено файлов: {len(extra_files)}")
    print()

    for item in extra_files:
        file_id = item['id']
        file_name = item['name']
        file_path = item['path']
        mime = item['mimeType']

        print(f"📦 {file_name} ({file_path or 'root'})")
        save_folder = determine_folder(file_path)
        folder_path = KNOWLEDGE_BASE_PATH / save_folder
        folder_path.mkdir(parents=True, exist_ok=True)

        try:
            raw = download_drive_file_bytes(drive_service, file_id)
            safe_base = sanitize_filename(file_name.replace('.xlsx', '').replace('.csv', ''))

            if mime == 'text/csv':
                out = folder_path / f"{safe_base}.csv"
                save_csv_bytes(raw, out)
                print(f"  ✅ CSV сохранён: {out.name}")
                stats['sheets_read'] += 1
                stats['success'] += 1
            elif mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                created = save_xlsx_bytes_as_csvs(raw, folder_path, safe_base)
                if created > 0:
                    print(f"  ✅ XLSX конвертирован в {created} CSV")
                    stats['sheets_read'] += created
                    stats['success'] += 1
                else:
                    print("  ⚠️ XLSX не конвертирован (см. предупреждения выше)")
                    stats['failed'] += 1
            elif mime == 'application/pdf':
                out = folder_path / f"{safe_base}.pdf"
                save_binary_bytes(raw, out)
                print(f"  ✅ PDF сохранён: {out.name}")
                stats['sheets_read'] += 1
                stats['success'] += 1
            else:
                print(f"  ⚠️ Неподдерживаемый mime: {mime}")
                stats['failed'] += 1
        except Exception as e:
            print(f"  ❌ Ошибка обработки файла: {e}")
            stats['failed'] += 1
        print()

    print("="*70)
    print(f"📊 Таблиц найдено: {stats['tables_found']}")
    print(f"📊 Таблиц обработано: {stats['success']}")
    print(f"📄 Листов прочитано: {stats['sheets_read']}")
    print(f"❌ Ошибок: {stats['failed']}")
    print("="*70)

    # Пост-обработка складского контура: карточки + Telegram summary
    pipeline = REPO_PATH / "PACK-warehouse" / "tools" / "warehouse_reports_pipeline.py"
    if pipeline.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(pipeline), "--hours", "6", "--send-telegram"],
                cwd=str(REPO_PATH),
                capture_output=True,
                text=True,
                check=False,
            )
            print("\n[warehouse-pipeline]")
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip())
            if result.returncode != 0:
                print(f"[warehouse-pipeline] non-zero exit: {result.returncode}")
        except Exception as e:
            print(f"[warehouse-pipeline] failed: {e}")

if __name__ == '__main__':
    main()
