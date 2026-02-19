#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Синхронизация Google Sheets → CSV → GitHub (с авторизацией)
Использует Google Drive API для доступа к приватным таблицам
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import io

# Настройки
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"

# Список таблиц: (SHEET_ID, GID, НАЗВАНИЕ, ПАПКА)
SHEETS = [
    # КУХНЯ
    ("1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU", "372408211", "Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ", "КУХНЯ"),
    ("1iHcpofQz8WjyPnYlAZOl6RKrh4MQze1T20d3npXMdJg", "0", "Калькулятор подсчета приготовленных продуктов", "КУХНЯ"),
    ("1JLmJ7KuSdj2reJlasvtFQekKrPb8-7yKZkPUEOMWFvE", "0", "Список продуктов учет", "КУХНЯ"),

    # БАР
    ("1xcbVugDZoUMrrDHQb_Dycbiq6mMBFvOiFPQV-uZo1Og", "0", "Калькуляции напитки", "БАР"),
    ("1J5BXZjLnAF3amAw02xH4MTYN5bPg9IwqOwnxqWBDJR4", "0", "Составы продукции", "БАР"),
    ("1s3PgusaFjJftN8oKpxiDUQewqcV-NzwiRzboFyK-0GA", "0", "Срок продукции", "БАР"),
    ("11BLOsP9Se5i-gNw5nrTkDPiikcRlGu3DYvsx6aqLzgo", "0", "Расчет смузи", "БАР"),

    # Чек-листы
    ("1WzFPsrsXIa3BewZOo2rC3vcCsjOSfzvaV099yBahM8c", "0", "чек-лист Тургенева", "БАР"),
    ("1w0xAzC20YSUPAmxYTezAIG0764uXMXOfMH1yqUPT1BA", "0", "чек-лист Самокиша", "БАР"),
    ("187eTXnt3i17vnnMeSX9KQHi5_qPuL7lQqGUehyfupds", "0", "чек-лист Луговая", "БАР"),
    ("1b_T5uST433dJGXnIlS4WNbIU0IDj1RymECZ8uMvITNk", "0", "Чек-лист Раннера Тургенева", "БАР"),
    ("1_0EDx54ziO4mW6jSKtyspux92t7OG5v6tc1kykc98bE", "0", "Чек-лист Раннера Самокиша", "БАР"),
    ("1J3kZ33YrBxXKW6WI2r6kl8kw51UHGTL3eKwJf3_Ri8s", "0", "Чек-лист Раннера Луговая", "БАР"),

    # Персонал
    ("1vA2XkU229QoRQhWAbqjGTeB1Ba_fFSp0Dq_CEhKZC7Y", "0", "Таблица по ЗП сотрудников", "Персонал"),
    ("1w4K9mrGmrSIua6oUI4kuMziI88YjLetJkcdjdzLADOE", "0", "Размер одежды сотрудников", "Персонал"),
    ("1KiXAyzk88L0fyOWp0C9IbEcI0QGAhQL7jmPJgE__aVU", "0", "ДР сотрудников и рабочая почта", "Персонал"),
    ("1pRFiKE3Ll6jTogDU-dgLgv2yKpNnMjxbJlwloBI4P-g", "0", "Список чатов кофейни", "Персонал"),
    ("1edkjH38zRhWnkovDImu__v5kJy-Fnrp6CVQhjxVc5wQ", "0", "Обратная связь по кофейне от сотрудников", "Персонал"),
    ("1ebAx2jvt0B7KHJhJBEJ_NUcXjgWxt3muChV7xitxhmk", "0", "Ответы Тестирование ДИ Официанта", "Персонал"),

    # ДЛЯ ШЕФА
    ("1kr6Z0HyYcAZWTTp7Jp_nopsGRVuK45smtcayBaTRPMM", "0", "Закуп сравнение цен", "ДЛЯ ШЕФА"),
    ("1h22FSh3F7dUGAIUDJXGbyOWQJokZ7jKVSh_aYt9pceI", "0", "Контакты печати строительных сеток", "ДЛЯ ШЕФА"),
    ("1fge42tcKdx33MNxH9jrQxxdmzAaoIeS8eCTbuFF4AMM", "0", "Компании по дезинсекции", "ДЛЯ ШЕФА"),
    ("1asLM0UlGNOOhQfMkoc5zDj2MKgtc4tWnwPSn5A3E9js", "0", "Расчет Диана МЕЛТ", "ДЛЯ ШЕФА"),
    ("1QrL48GAzpVABqwwSO5z80PNZNk2cVKXLwDYwEGXz5sM", "0", "График оплаты поставщиков", "ДЛЯ ШЕФА"),

    # Инвентаризация
    ("1-MMMX8UrxvrRhwDwkN5K94bdf95YG1bAEtGQ9kwvV6I", "0", "Список посуды", "Инвентаризация "),
    ("1OhCnZGMgDEx-ghU-F-0VCP3xloGQO37mrzlJ1SnsbIU", "0", "Отчет по инвентаризации", "Инвентаризация "),
    ("1sqrYyqSENH83Q-O9BWtUUAYpAWa63JHyvpp2NZuGUIg", "0", "Список зерна по кофейням", "Инвентаризация "),
]

stats = {
    'success': 0,
    'failed': 0,
    'updated': 0,
    'unchanged': 0
}

def get_credentials():
    """Получение учетных данных Google Drive API"""
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
            if not credentials_path.exists():
                print("❌ Файл credentials.json не найден!")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def export_sheet_to_csv(service, sheet_id, gid):
    """Экспорт Google Sheet в CSV через API"""
    try:
        # Экспорт через Google Drive API
        request = service.files().export_media(
            fileId=sheet_id,
            mimeType='text/csv'
        )

        fh = io.BytesIO()
        from googleapiclient.http import MediaIoBaseDownload
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        return fh.getvalue().decode('utf-8')
    except Exception as e:
        print(f"  ❌ Ошибка экспорта: {e}")
        return None

def main():
    print("="*60)
    print("🔄 СИНХРОНИЗАЦИЯ GOOGLE SHEETS (с авторизацией)")
    print("="*60)
    print()

    # Получение учетных данных
    print("🔑 Получение учетных данных...")
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    print("✅ Авторизация успешна")
    print()

    # Синхронизация таблиц
    for sheet_id, gid, name, folder in SHEETS:
        print(f"📥 Синхронизация: {name}")

        # Создать папку
        folder_path = KNOWLEDGE_BASE_PATH / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Путь к файлу
        file_path = folder_path / f"{name}.csv"

        # Экспорт таблицы
        csv_content = export_sheet_to_csv(service, sheet_id, gid)

        if csv_content is None:
            stats['failed'] += 1
            continue

        # Проверить изменения
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                old_content = f.read()

            if old_content == csv_content:
                print("  ⏭️  Без изменений")
                stats['unchanged'] += 1
                continue

        # Сохранить файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        if file_path.exists() and file_path.stat().st_size > 0:
            print("  ✅ Обновлён")
            stats['updated'] += 1
            stats['success'] += 1
        else:
            print("  ✅ Создан")
            stats['success'] += 1

    print()
    print("="*60)
    print(f"📊 Успешно: {stats['success']} | Ошибок: {stats['failed']}")
    print(f"🔄 Обновлено: {stats['updated']} | Без изменений: {stats['unchanged']}")
    print("="*60)

if __name__ == '__main__':
    main()
