#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ФИНАЛЬНАЯ синхронизация Google Sheets → CSV
Читает ВСЕ листы из каждой таблицы через Sheets API
"""

import os
import sys
from pathlib import Path
import pickle
import csv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"

# Список таблиц: (SHEET_ID, НАЗВАНИЕ, ПАПКА)
SHEETS = [
    # КУХНЯ
    ("1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU", "Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ", "КУХНЯ"),
    ("1iHcpofQz8WjyPnYlAZOl6RKrh4MQze1T20d3npXMdJg", "Калькулятор подсчета приготовленных продуктов", "КУХНЯ"),
    ("1JLmJ7KuSdj2reJlasvtFQekKrPb8-7yKZkPUEOMWFvE", "Список продуктов учет", "КУХНЯ"),

    # БАР
    ("1xcbVugDZoUMrrDHQb_Dycbiq6mMBFvOiFPQV-uZo1Og", "Калькуляции напитки", "БАР"),
    ("1J5BXZjLnAF3amAw02xH4MTYN5bPg9IwqOwnxqWBDJR4", "Составы продукции", "БАР"),
    ("1s3PgusaFjJftN8oKpxiDUQewqcV-NzwiRzboFyK-0GA", "Срок продукции", "БАР"),
]

stats = {'success': 0, 'failed': 0, 'sheets_read': 0}

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

def get_sheet_names(service, sheet_id):
    """Получить названия всех листов в таблице"""
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        return [sheet['properties']['title'] for sheet in sheets]
    except Exception as e:
        print(f"  ❌ Ошибка получения листов: {e}")
        return []

def read_sheet_data(service, sheet_id, sheet_name):
    """Чтение данных из конкретного листа"""
    try:
        result = service.spreadsheets().values().get(
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

def main():
    print("="*70)
    print("🔄 ФИНАЛЬНАЯ СИНХРОНИЗАЦИЯ GOOGLE SHEETS")
    print("="*70)
    print()

    # Авторизация
    print("🔑 Авторизация...")
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    print("✅ Авторизация успешна")
    print()

    # Синхронизация
    for sheet_id, table_name, folder in SHEETS:
        print(f"📊 {table_name}")

        # Создать папку
        folder_path = KNOWLEDGE_BASE_PATH / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Получить все листы
        sheet_names = get_sheet_names(service, sheet_id)

        if not sheet_names:
            print(f"  ❌ Не удалось получить листы")
            stats['failed'] += 1
            continue

        print(f"  📄 Найдено листов: {len(sheet_names)}")

        # Читать каждый лист
        for sheet_name in sheet_names:
            print(f"    📥 {sheet_name}...", end=" ")

            data = read_sheet_data(service, sheet_id, sheet_name)

            if data is None:
                stats['failed'] += 1
                continue

            if not data:
                print("⚠️  Пустой")
                continue

            # Сохранить CSV
            safe_name = sheet_name.replace('/', '-').replace('\\', '-')
            file_path = folder_path / f"{table_name} - {safe_name}.csv"
            save_as_csv(data, file_path)

            print(f"✅ ({len(data)} строк)")
            stats['sheets_read'] += 1

        stats['success'] += 1
        print()

    print("="*70)
    print(f"📊 Таблиц обработано: {stats['success']}")
    print(f"📄 Листов прочитано: {stats['sheets_read']}")
    print(f"❌ Ошибок: {stats['failed']}")
    print("="*70)

if __name__ == '__main__':
    main()
