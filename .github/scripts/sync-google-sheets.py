#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
АВТОМАТИЧЕСКАЯ синхронизация ВСЕХ Google Sheets из папки Drive
Находит все таблицы автоматически, не нужно добавлять вручную
"""

import os
import sys
from pathlib import Path
import pickle
import csv
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"

# ID папки Google Drive
DRIVE_FOLDER_ID = "120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC"

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
        results = drive_service.files().list(
            q=query,
            fields="files(id, name, mimeType, parents)",
            pageSize=1000
        ).execute()

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

def get_sheet_names(sheets_service, sheet_id):
    """Получить названия всех листов в таблице"""
    try:
        sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        return [sheet['properties']['title'] for sheet in sheets]
    except Exception as e:
        print(f"  ❌ Ошибка получения листов: {e}")
        return []

def read_sheet_data(sheets_service, sheet_id, sheet_name):
    """Чтение данных из конкретного листа"""
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=f"'{sheet_name}'"
        ).execute()

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

    # Поиск всех таблиц
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
