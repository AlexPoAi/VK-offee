"""
Скрипт для перехвата API запросов Saby
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

print("🚀 Браузер запущен")
print("📖 Открываю https://online.sbis.ru")
driver.get('https://online.sbis.ru')

print("\n" + "="*60)
print("⏸️  Войди в систему (60 секунд)")
print("="*60)

for i in range(60, 0, -5):
    print(f"⏳ {i} сек...")
    time.sleep(5)

print("\n📡 Перехватываю API запросы...")

# Перейти в раздел Товары
driver.get('https://online.sbis.ru/page/goods')
time.sleep(5)

# Получить логи
logs = driver.get_log('performance')

api_requests = []
for entry in logs:
    log = json.loads(entry['message'])['message']
    if log['method'] == 'Network.responseReceived':
        url = log['params']['response']['url']
        if 'service' in url or 'api' in url or 'json' in url.lower():
            api_requests.append({
                'url': url,
                'method': log['params']['response'].get('requestHeaders', {}).get(':method', 'GET'),
                'status': log['params']['response']['status']
            })

print(f"\n✅ Найдено {len(api_requests)} API запросов:")
for req in api_requests[:20]:  # Первые 20
    print(f"  {req['method']} {req['url'][:100]}")

# Сохранить в файл
with open('api_requests.json', 'w', encoding='utf-8') as f:
    json.dump(api_requests, f, indent=2, ensure_ascii=False)

print("\n✅ Сохранено в api_requests.json")

time.sleep(30)
driver.quit()
print("🔒 Готово")
