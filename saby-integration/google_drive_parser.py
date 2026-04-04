"""
Google Drive Parser для данных из Saby Presto
Читает Excel/CSV файлы с Google Drive и парсит данные

ПАПКА GOOGLE DRIVE (для бота / Жанна):
https://drive.google.com/drive/folders/1sGGcG1DBHIMMhZFvPGd_gGOesncQwhiq
Folder ID: 1sGGcG1DBHIMMhZFvPGd_gGOesncQwhiq
"""

import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pickle
from datetime import datetime

# Scopes для Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class SabyGoogleDriveParser:
    def __init__(self, credentials_file='credentials.json'):
        """
        Инициализация парсера

        Args:
            credentials_file: Путь к файлу credentials.json из Google Cloud Console
        """
        self.credentials_file = credentials_file
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Аутентификация в Google Drive API"""
        creds = None

        # Токен сохраняется в token.pickle после первой авторизации
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # Если нет валидных credentials, запросить авторизацию
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Сохранить credentials для следующего запуска
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Авторизация в Google Drive успешна")

    def list_files_in_folder(self, folder_id, file_type='xlsx'):
        """
        Получить список файлов в папке

        Args:
            folder_id: ID папки в Google Drive
            file_type: Тип файлов (xlsx, csv)

        Returns:
            List of file metadata
        """
        query = f"'{folder_id}' in parents and mimeType contains '{file_type}'"

        results = self.service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, createdTime, modifiedTime)"
        ).execute()

        files = results.get('files', [])
        return files

    def download_file(self, file_id, file_name):
        """
        Скачать файл с Google Drive

        Args:
            file_id: ID файла
            file_name: Имя для сохранения

        Returns:
            Path to downloaded file
        """
        request = self.service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Сохранить файл
        with open(file_name, 'wb') as f:
            f.write(fh.getvalue())

        return file_name

    def parse_goods(self, file_path):
        """
        Парсить файл с товарами

        Args:
            file_path: Путь к Excel/CSV файлу

        Returns:
            DataFrame с товарами
        """
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Предполагаемые колонки (нужно адаптировать под реальный формат)
        # Пример: Код, Название, Цена, Категория

        print(f"📦 Загружено товаров: {len(df)}")
        return df

    def parse_sales(self, file_path):
        """
        Парсить файл с продажами

        Args:
            file_path: Путь к Excel/CSV файлу

        Returns:
            DataFrame с продажами
        """
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        print(f"💰 Загружено продаж: {len(df)}")
        return df

    def parse_stock(self, file_path):
        """
        Парсить файл с остатками

        Args:
            file_path: Путь к Excel/CSV файлу

        Returns:
            DataFrame с остатками
        """
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        print(f"📊 Загружено остатков: {len(df)}")
        return df

    def get_latest_file(self, folder_id, prefix='goods'):
        """
        Получить последний файл из папки

        Args:
            folder_id: ID папки
            prefix: Префикс имени файла

        Returns:
            File metadata or None
        """
        files = self.list_files_in_folder(folder_id)

        # Фильтровать по префиксу
        matching_files = [f for f in files if f['name'].startswith(prefix)]

        if not matching_files:
            return None

        # Сортировать по дате изменения (последний)
        latest = sorted(matching_files, key=lambda x: x['modifiedTime'], reverse=True)[0]
        return latest

    def sync_data(self, folders_config):
        """
        Синхронизировать все данные из Google Drive

        Args:
            folders_config: Dict с ID папок
                {
                    'goods': 'folder_id_1',
                    'sales': 'folder_id_2',
                    'stock': 'folder_id_3'
                }

        Returns:
            Dict с DataFrame для каждого типа данных
        """
        data = {}

        # Товары
        if 'goods' in folders_config:
            print("\n📦 Синхронизация товаров...")
            latest = self.get_latest_file(folders_config['goods'], 'goods')
            if latest:
                file_path = self.download_file(latest['id'], f"temp_{latest['name']}")
                data['goods'] = self.parse_goods(file_path)
                os.remove(file_path)

        # Продажи
        if 'sales' in folders_config:
            print("\n💰 Синхронизация продаж...")
            latest = self.get_latest_file(folders_config['sales'], 'sales')
            if latest:
                file_path = self.download_file(latest['id'], f"temp_{latest['name']}")
                data['sales'] = self.parse_sales(file_path)
                os.remove(file_path)

        # Остатки
        if 'stock' in folders_config:
            print("\n📊 Синхронизация остатков...")
            latest = self.get_latest_file(folders_config['stock'], 'stock')
            if latest:
                file_path = self.download_file(latest['id'], f"temp_{latest['name']}")
                data['stock'] = self.parse_stock(file_path)
                os.remove(file_path)

        return data


# Пример использования
if __name__ == '__main__':
    # Инициализация парсера
    parser = SabyGoogleDriveParser('credentials.json')

    # Конфигурация папок (ID папок из Google Drive)
    folders = {
        'goods': 'YOUR_GOODS_FOLDER_ID',
        'sales': 'YOUR_SALES_FOLDER_ID',
        'stock': 'YOUR_STOCK_FOLDER_ID'
    }

    # Синхронизация данных
    data = parser.sync_data(folders)

    # Использование данных
    if 'goods' in data:
        print("\n📦 Товары:")
        print(data['goods'].head())

    if 'sales' in data:
        print("\n💰 Продажи:")
        print(data['sales'].head())

    if 'stock' in data:
        print("\n📊 Остатки:")
        print(data['stock'].head())
