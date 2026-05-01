#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт синхронизации Google Drive → GitHub (улучшенная версия)
Автоматическая синхронизация документов из Google Drive в репозиторий VK-offee
Версия 2.0 с поддержкой UTF-8 и Pack/Downstream архитектуры
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
import chardet

# Настройки
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC')
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"
SYNC_REPORTS_PATH = Path(__file__).parent / "reports"
REPORT_PATH = SYNC_REPORTS_PATH / f"sync-{datetime.now().strftime('%Y-%m-%d')}.md"
SYNC_REPORTS_ENABLED = os.getenv('SYNC_REPORTS_ENABLED', '0') == '1'

if SYNC_REPORTS_ENABLED:
    SYNC_REPORTS_PATH.mkdir(parents=True, exist_ok=True)

# Статистика
stats = {
    'downloaded': 0,
    'updated': 0,
    'skipped': 0,
    'errors': 0,
    'error_files': [],
    'encoding_fixed': 0,
    'total_size': 0
}

IGNORED_ROOT_PREFIXES = (
    "Отчет синхронизации ",
    "Отчёт синхронизации ",
)
IGNORED_PATH_PREFIXES = (
    "sync-reports/",
)

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

def fix_encoding(content_bytes):
    """Исправление кодировки: автоопределение и конвертация в UTF-8"""
    try:
        # Пробуем определить кодировку
        detected = chardet.detect(content_bytes)
        encoding = detected['encoding']

        if encoding and encoding.lower() != 'utf-8':
            # Конвертируем в UTF-8
            text = content_bytes.decode(encoding, errors='ignore')
            content_bytes = text.encode('utf-8')
            stats['encoding_fixed'] += 1
            return content_bytes, True

        return content_bytes, False
    except Exception as e:
        print(f"  ⚠️  Ошибка исправления кодировки: {e}")
        return content_bytes, False

def list_files(service, folder_id, path=""):
    """Рекурсивный список файлов в папке"""
    files = []

    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, modifiedTime, size)",
        orderBy="name"
    ).execute()

    items = results.get('files', [])

    for item in items:
        item_path = f"{path}/{item['name']}" if path else item['name']

        if any(item_path.startswith(prefix) for prefix in IGNORED_PATH_PREFIXES):
            stats['skipped'] += 1
            continue

        if not path and item['name'].startswith(IGNORED_ROOT_PREFIXES):
            stats['skipped'] += 1
            continue

        # Если это папка, рекурсивно обходим
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            files.extend(list_files(service, item['id'], item_path))
        else:
            files.append({
                'id': item['id'],
                'name': item['name'],
                'path': item_path,
                'mimeType': item['mimeType'],
                'modifiedTime': item['modifiedTime'],
                'size': item.get('size', 0)
            })

    return files

def download_file(service, file_id, file_path, mime_type):
    """Скачивание файла с Google Drive с правильной кодировкой"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Google Docs форматы экспортируем
        if mime_type.startswith('application/vnd.google-apps'):
            if 'document' in mime_type:
                # Google Docs → Markdown
                request = service.files().export_media(fileId=file_id, mimeType='text/plain')
                file_path = file_path.with_suffix('.md')
            elif 'spreadsheet' in mime_type:
                # Google Sheets → CSV
                request = service.files().export_media(fileId=file_id, mimeType='text/csv')
                file_path = file_path.with_suffix('.csv')
            elif 'presentation' in mime_type:
                # Google Slides → PDF
                request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
                file_path = file_path.with_suffix('.pdf')
            else:
                print(f"  ⏭️  Пропущен (неподдерживаемый тип Google Apps)")
                stats['skipped'] += 1
                return
        else:
            # Обычные файлы скачиваем как есть
            request = service.files().get_media(fileId=file_id)

        # Скачивание в память
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Получаем содержим��е
        content = fh.getvalue()

        # Исправляем кодировку для текстовых файлов
        if file_path.suffix in ['.md', '.txt', '.csv']:
            content, was_fixed = fix_encoding(content)
            if was_fixed:
                print(f"  🔧 Исправлена кодировка")

        # Проверяем, изменился ли файл
        if file_path.exists():
            with open(file_path, 'rb') as f:
                existing_content = f.read()
            if existing_content == content:
                print(f"  ⏭️  Без изменений")
                stats['skipped'] += 1
                return
            else:
                print(f"  🔄 Обновлён")
                stats['updated'] += 1
        else:
            print(f"  ✅ Скачан")
            stats['downloaded'] += 1

        # Сохраняем файл
        with open(file_path, 'wb') as f:
            f.write(content)

        stats['total_size'] += len(content)

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        stats['errors'] += 1
        stats['error_files'].append(str(file_path))

def generate_report():
    """Генерация отчета о синхронизации"""
    report = f"""# Отчёт о синхронизации

**Дата:** {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}
**Длительность:** {stats['total_size'] / 1024:.2f} КБ
**Файлов:** {stats['downloaded'] + stats['updated'] + stats['skipped']}
**Ошибок:** {stats['errors']}

## 📊 Статистика

- ✅ Скачано новых: {stats['downloaded']}
- 🔄 Обновлено: {stats['updated']}
- ⏭️  Пропущено (без изменений): {stats['skipped']}
- 🔧 Исправлена кодировка: {stats['encoding_fixed']}
- ❌ Ошибок: {stats['errors']}

## 📦 Архитектура Pack/Downstream

Этот репозиторий — **Pack** (Вторые принципы):
- Source-of-truth для домена кофеен
- Формализованное знание
- Структура SRT (F0-F9)

Google Drive → knowledge-base/ → рабочие документы
content/ → формализованное знание (Pack)

## 🔗 Связь с Downstream

Downstream репозиторий: `creativ-convector`
- Обработка заметок
- Стратегирование
- Извлечение знаний для Pack

"""

    if stats['error_files']:
        report += "\n## ❌ Файлы с ошибками\n\n"
        for file in stats['error_files']:
            report += f"- {file}\n"

    report += f"\n---\n\n**Следующая синхронизация:** Запустите `python3 .github/scripts/sync_google_drive.py`\n"

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 Отчёт сохранён: {REPORT_PATH.relative_to(REPO_PATH)}")

def main():
    """Главная функция"""
    print("="*60)
    print("🔄 СИНХРОНИЗАЦИЯ GOOGLE DRIVE → VK-OFFEE (PACK)")
    print("="*60 + "\n")
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

    if SYNC_REPORTS_ENABLED:
        generate_report()
    else:
        print("\n📄 Локальный sync-report отключён (SYNC_REPORTS_ENABLED=1 чтобы включить)")

    # Итоговая статистика
    print(f"\n" + "="*60)
    print(f"✅ СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА")
    print("="*60)
    print(f"📥 Скачано новых: {stats['downloaded']}")
    print(f"🔄 Обновлено: {stats['updated']}")
    print(f"⏭️  Пропущено: {stats['skipped']}")
    print(f"🔧 Исправлена кодировка: {stats['encoding_fixed']}")
    print(f"❌ Ошибок: {stats['errors']}")
    print(f"💾 Общий размер: {stats['total_size'] / 1024:.2f} КБ")

if __name__ == '__main__':
    main()
