#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт загрузки документов из GitHub → Google Drive
Конвертация Markdown → Google Docs
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import markdown
from io import BytesIO

# Настройки
SCOPES = ['https://www.googleapis.com/auth/drive.file']
DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC')
REPO_PATH = Path(__file__).parent.parent.parent

# Статистика
stats = {
    'uploaded': 0,
    'updated': 0,
    'errors': 0,
    'error_files': []
}

def get_credentials():
    """Получение учетных данных Google Drive API с правами на запись"""
    creds = None
    token_path = Path(__file__).parent / 'token_upload.pickle'

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
                print(f"❌ Файл credentials.json не найден: {credentials_path}")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохранение учетных данных
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def markdown_to_html(md_content):
    """Конвертация Markdown в HTML для Google Docs"""
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    return html

def find_or_create_folder(service, folder_name, parent_id=None):
    """Найти или создать папку на Google Drive"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    folders = results.get('files', [])

    if folders:
        return folders[0]['id']

    # Создать папку
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    print(f"✅ Создана папка: {folder_name}")
    return folder.get('id')

def upload_markdown_as_google_doc(service, md_file_path, folder_id, doc_name=None):
    """Загрузить Markdown файл как Google Doc"""
    try:
        # Прочитать Markdown
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Конвертировать в HTML
        html_content = markdown_to_html(md_content)

        # Имя документа
        if not doc_name:
            doc_name = Path(md_file_path).stem

        # Проверить, существует ли документ
        query = f"name='{doc_name}' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.document'"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        existing_files = results.get('files', [])

        # Создать временный HTML файл
        temp_html = Path('/tmp') / f"{doc_name}.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

        file_metadata = {
            'name': doc_name,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }

        media = MediaFileUpload(
            str(temp_html),
            mimetype='text/html',
            resumable=True
        )

        if existing_files:
            # Обновить существующий документ
            file_id = existing_files[0]['id']
            service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            print(f"✅ Обновлён: {doc_name}")
            stats['updated'] += 1
        else:
            # Создать новый документ
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"✅ Загружен: {doc_name}")
            stats['uploaded'] += 1

        # Удалить временный файл
        temp_html.unlink()

    except Exception as e:
        print(f"❌ Ошибка при загрузке {md_file_path}: {e}")
        stats['errors'] += 1
        stats['error_files'].append(str(md_file_path))

def main():
    """Основная функция"""
    print("🚀 Загрузка документов на Google Drive...")
    print(f"📁 Репозиторий: {REPO_PATH}")

    # Получить credentials
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Создать структуру папок
    root_folder_id = DRIVE_FOLDER_ID

    # БАР/
    bar_folder_id = find_or_create_folder(service, 'БАР', root_folder_id)

    # БАР/Должностные инструкции/
    di_folder_id = find_or_create_folder(service, 'Должностные инструкции', bar_folder_id)

    # БАР/Матрицы ответственности/
    matrix_folder_id = find_or_create_folder(service, 'Матрицы ответственности', bar_folder_id)

    # Загрузить документы
    print("\n📤 Загрузка документов...")

    # 1. Должностная инструкция Бариста
    barista_di = REPO_PATH / 'knowledge-base' / 'БАР' / 'Должностная инструкция Бариста.md'
    if barista_di.exists():
        upload_markdown_as_google_doc(
            service,
            barista_di,
            di_folder_id,
            'Должностная инструкция Бариста'
        )

    # 2. Матрица ответственности
    matrix = REPO_PATH / 'knowledge-base' / 'БАР' / 'Матрица ответственности Бариста-Официант.md'
    if matrix.exists():
        upload_markdown_as_google_doc(
            service,
            matrix,
            matrix_folder_id,
            'Матрица ответственности Бариста-Официант'
        )

    # Статистика
    print("\n" + "="*50)
    print("📊 СТАТИСТИКА ЗАГРУЗКИ")
    print("="*50)
    print(f"✅ Загружено новых: {stats['uploaded']}")
    print(f"🔄 Обновлено: {stats['updated']}")
    print(f"❌ Ошибок: {stats['errors']}")

    if stats['error_files']:
        print("\n❌ Файлы с ошибками:")
        for f in stats['error_files']:
            print(f"  - {f}")

    print("\n✅ Загрузка завершена!")

if __name__ == '__main__':
    main()
