#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление главного файла "Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ"
Скачивание через Google Sheets API вместо прямой ссылки
"""

import pickle
import csv
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU'
REPO_PATH = Path(__file__).parent.parent.parent
OUTPUT_FILE = REPO_PATH / "knowledge-base" / "КУХНЯ" / "Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ.csv"

def get_credentials():
    token_path = Path(__file__).parent / 'token.pickle'
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def main():
    print("🔧 Исправление главного файла...")

    # Авторизация
    creds = get_credentials()
    sheets_service = build('sheets', 'v4', credentials=creds)

    # Получить метаданные таблицы
    sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    table_name = sheet_metadata['properties']['title']
    sheets = sheet_metadata.get('sheets', [])

    print(f"📊 Таблица: {table_name}")
    print(f"📄 Листов: {len(sheets)}")

    # Найти главный лист (обычно первый или с названием "Оглавление")
    main_sheet = None
    for sheet in sheets:
        sheet_title = sheet['properties']['title']
        if 'оглавление' in sheet_title.lower() or sheet['properties']['index'] == 0:
            main_sheet = sheet_title
            break

    if not main_sheet:
        main_sheet = sheets[0]['properties']['title']

    print(f"📥 Скачиваю лист: {main_sheet}")

    # Читаем данные
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"'{main_sheet}'"
    ).execute()

    values = result.get('values', [])

    if not values:
        print("❌ Лист пустой!")
        return

    # Сохраняем в CSV
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(values)

    print(f"✅ Сохранено: {OUTPUT_FILE}")
    print(f"📊 Строк: {len(values)}")

if __name__ == '__main__':
    main()
