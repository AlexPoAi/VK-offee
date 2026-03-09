"""
Тестовый скрипт для проверки подключения к Saby API
"""

import requests
import json
import os
from dotenv import load_dotenv

# Загрузить .env
load_dotenv()

# Реальные параметры из документации
AUTH_URL = "https://online.sbis.ru/oauth/service/"

# Credentials из .env
APP_CLIENT_ID = os.getenv('SABY_APP_CLIENT_ID')
APP_SECRET = os.getenv('SABY_APP_SECRET')
SECRET_KEY = os.getenv('SABY_SECRET_KEY')

print("🔍 Тестирование подключения к Saby API")
print(f"URL: {AUTH_URL}")
print(f"Client ID: {APP_CLIENT_ID[:10]}..." if APP_CLIENT_ID else "❌ Не задан")

# Проверка что credentials заданы
if not all([APP_CLIENT_ID, APP_SECRET, SECRET_KEY]):
    print("\n❌ Ошибка: Не все credentials заданы в .env файле")
    print("Нужны: SABY_APP_CLIENT_ID, SABY_APP_SECRET, SABY_SECRET_KEY")
    print("\nСначала нужно:")
    print("1. Войти в https://online.sbis.ru")
    print("2. Зарегистрировать приложение")
    print("3. Получить credentials")
    print("4. Добавить их в .env файл")
    exit(1)

# Попытка авторизации
print("\n📡 Отправка запроса на авторизацию...")

payload = {
    "app_client_id": APP_CLIENT_ID,
    "app_secret": APP_SECRET,
    "secret_key": SECRET_KEY
}

try:
    response = requests.post(AUTH_URL, json=payload, timeout=10)

    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text[:200]}")

    if response.status_code == 200:
        data = response.json()
        if 'token' in data:
            token = data['token']
            print(f"\n✅ Авторизация успешна!")
            print(f"Токен получен: {token[:20]}...")

            # Сохранить токен для дальнейшего использования
            with open('.token', 'w') as f:
                f.write(token)
            print("Токен сохранён в .token")
        else:
            print(f"\n⚠️ Токен не найден в ответе: {data}")
    else:
        print(f"\n❌ Ошибка авторизации: {response.status_code}")
        print(f"Ответ: {response.text}")

except requests.exceptions.Timeout:
    print("\n❌ Таймаут подключения")
except requests.exceptions.ConnectionError:
    print("\n❌ Ошибка подключения к серверу")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
