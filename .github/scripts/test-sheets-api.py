#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Синхронизация Google Sheets → CSV (через Sheets API)
Читает данные напрямую из таблиц с авторизацией
"""

import os
import sys
from pathlib import Path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import csv

# Настройки
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"

# Список таблиц: (SHEET_ID, RANGE, НАЗВАНИЕ, ПАПКА)
# RANGE = название листа или "Sheet1" для первого листа
SHEETS = [
    # КУХНЯ
    ("1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU", "Себестоимость кухня", "Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ", "КУХНЯ"),
    ("1iHcpofQz8WjyPnYlAZOl6RKrh4MQze1T20d3npXMdJg", "Sheet1", "Калькулятор подсчета приготовленных продуктов", "КУХНЯ"),
    ("1JLmJ7KuSdj2reJlasvtFQekKrPb8-7yKZkPUEOMWFvE", "Sheet1", "Список продуктов учет", "КУХНЯ"),

    # БАР
    ("1xcbVugDZoUMrrDHQb_Dycbiq6mMBFvOiFPQV-uZo1Og", "Sheet1", "Калькуляции напитки", "БАР"),
    ("1J5BXZjLnAF3amAw02xH4MTYN5bPg9IwqOwnxqWBDJR4", "Sheet1", "Составы продукции", "БАР"),
    ("1s3PgusaFjJftN8oKpxiDUQewqcV-NzwiRzboFyK-0GA", "Sheet1", "Срок продукции", "БАР"),
]

stats = {'success': 0, 'failed': 0, 'updated': 0}

def get_credentials():
    """Получение учетных данных"""
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
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def read_sheet_data(service, sheet_id, range_name):
    """Чтение данных из Google Sheet"""
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"  ❌ Ошибка чтения: {e}")
        return None

def save_as_csv(data, file_path):
    """Сохранение данных в CSV"""
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    print("="*60)
    print("🔄 СИНХРОНИЗАЦИЯ GOOGLE SHEETS (Sheets API)")
    print("="*60)
    print()

    # Авторизация
    print("🔑 Авторизация...")
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    print("✅ Авторизация успешна")
    print()

    # Синхронизация
    for sheet_id, range_name, name, folder in SHEETS:
        print(f"📥 {name}")

        # Создать папку
        folder_path = KNOWLEDGE_BASE_PATH / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / f"{name}.csv"

        # Читать данные
        data = read_sheet_data(service, sheet_id, range_name)

        if data is None:
            stats['failed'] += 1
            continue

        if not data:
            print(f"  ⚠️  Таблица пустая")
            stats['failed'] += 1
            continue

        # Сохранить CSV
        save_as_csv(data, file_path)
        print(f"  ✅ Сохранено ({len(data)} строк)")
        stats['success'] += 1
        stats['updated'] += 1

    print()
    print("="*60)
    print(f"📊 Успешно: {stats['success']} | Ошибок: {stats['failed']}")
    print("="*60)

if __name__ == '__main__':
    main()
