#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт синхронизации Google Drive → GitHub
Автоматическая синхронизация документов из Google Drive в репозиторий VK-offee
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pickle
import io

# Настройки
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC')
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"
REPORT_PATH = KNOWLEDGE_BASE_PATH / f"Отчет синхронизации {datetime.now().strftime('%d.%m.%Y')}.md"

# Статистика
stats = {
    'downloaded': 0,
    'skipped': 0,
    'errors': 0,
    'error_files': []
}

def get_credentials():
    """Получение учетных данных Google Drive API"""
    creds = None
    token_path = Path(__file__).parent / 'token.pickle'

    # Загрузка сохраненных учетных данных
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Если нет валидных учетных данных, запросить авторизацию
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = Path(__file__).parent / 'credentials.json'
            if not credentials_path.exists():
                print("❌ Файл credentials.json не найден!")
                print("📝 Инструкция:")
                print("1. Перейдите на https://console.cloud.google.com/")
                print("2. Создайте проект и включите Google Drive API")
                print("3. Создайте OAuth 2.0 Client ID")
                print("4. Скачайте credentials.json в папку .github/scripts/")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохранение учетных данных
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def list_files(service, folder_id, path=""):
    """Рекурсивный список файлов в папке"""
    files = []

    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, modifiedTime)",
        orderBy="name"
    ).execute()

    items = results.get('files', [])

    for item in items:
        file_path = f"{path}/{item['name']}" if path else item['name']

        if item['mimeType'] == 'application/vnd.google-apps.folder':
            # Рекурсивно обработать подпапку
            files.extend(list_files(service, item['id'], file_path))
        else:
            files.append({
                'id': item['id'],
                'name': item['name'],
                'path': file_path,
                'mimeType': item['mimeType'],
                'modifiedTime': item['modifiedTime']
            })

    return files

def download_file(service, file_id, file_path, mime_type):
    """Скачивание файла из Google Drive"""
    try:
        # Создание директории
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Google Docs форматы нужно экспортировать
        if mime_type.startswith('application/vnd.google-apps'):
            if 'document' in mime_type:
                request = service.files().export_media(fileId=file_id, mimeType='text/markdown')
                file_path = file_path.with_suffix('.md')
            elif 'spreadsheet' in mime_type:
                request = service.files().export_media(fileId=file_id, mimeType='text/csv')
                file_path = file_path.with_suffix('.csv')
            elif 'presentation' in mime_type:
                request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
                file_path = file_path.with_suffix('.pdf')
            else:
                print(f"⚠️  Пропуск {file_path.name} (неподдерживаемый тип Google Apps)")
                stats['skipped'] += 1
                return False
        else:
            request = service.files().get_media(fileId=file_id)

        # Скачивание
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

        # Сохранение
        with open(file_path, 'wb') as f:
            f.write(fh.getvalue())

        print(f"✅ {file_path.name}")
        stats['downloaded'] += 1
        return True

    except Exception as e:
        print(f"❌ Ошибка при скачивании {file_path.name}: {e}")
        stats['errors'] += 1
        stats['error_files'].append(f"{file_path.name}: {str(e)}")
        return False

def generate_report():
    """Генерация отчета о синхронизации"""
    report = f"""# Отчет синхронизации {datetime.now().strftime('%d.%m.%Y')}

**Дата:** {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}

**Скачано файлов:** {stats['downloaded']}

**Пропущено:** {stats['skipped']}

**Ошибок:** {stats['errors']}

"""

    if stats['error_files']:
        report += "## Ошибки\n\n"
        for error in stats['error_files']:
            report += f"- {error}\n"

    # Сохранение отчета
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📊 Отчет сохранен: {REPORT_PATH}")

def main():
    """Основная функция"""
    print("🔄 Синхронизация Google Drive → GitHub", flush=True)
    print(f"📁 Папка Drive: {DRIVE_FOLDER_ID}", flush=True)
    print(f"📂 Локальный путь: {KNOWLEDGE_BASE_PATH}\n", flush=True)

    # Получение учетных данных
    print("🔑 Получение учетных данных...", flush=True)
    creds = get_credentials()
    print("✅ Учетные данные получены", flush=True)

    print("🔌 Подключение к Google Drive API...", flush=True)
    service = build('drive', 'v3', credentials=creds)
    print("✅ Подключение установлено", flush=True)

    # Получение списка файлов
    print("📋 Получение списка файлов...", flush=True)
    files = list_files(service, DRIVE_FOLDER_ID)
    print(f"Найдено файлов: {len(files)}\n", flush=True)

    # Скачивание файлов
    print("⬇️  Скачивание файлов...\n", flush=True)
    for i, file in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {file['path']}", flush=True)
        file_path = KNOWLEDGE_BASE_PATH / file['path']
        download_file(service, file['id'], file_path, file['mimeType'])

    # Генерация отчета
    generate_report()

    # Итоговая статистика
    print(f"\n✅ Синхронизация завершена!")
    print(f"📥 Скачано: {stats['downloaded']}")
    print(f"⏭️  Пропущено: {stats['skipped']}")
    print(f"❌ Ошибок: {stats['errors']}")

if __name__ == '__main__':
    main()
