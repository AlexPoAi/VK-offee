"""
Полуавтоматический скрипт для работы с Saby Presto
Ты вводишь логин/пароль вручную, скрипт делает остальное
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("🚀 Запуск браузера...")

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

try:
    # Открыть страницу входа
    print("📖 Открываю https://online.sbis.ru")
    driver.get('https://online.sbis.ru')

    print("\n" + "="*60)
    print("⏸️  ПАУЗА: Войди в систему вручную")
    print("="*60)
    print("1. Введи email: vkusnyycoffee@gmail.com")
    print("2. Введи пароль")
    print("3. Нажми 'Войти'")
    print("4. Дождись загрузки главной страницы")
    print("="*60)

    input("\n✅ Нажми Enter когда войдёшь в систему...")

    print("\n📸 Делаю скриншот главной страницы...")
    driver.save_screenshot('main_page.png')
    print("✅ Сохранено: main_page.png")

    # Попробовать перейти в раздел Товары
    print("\n📦 Пытаюсь перейти в раздел 'Товары'...")
    driver.get('https://online.sbis.ru/page/goods')
    time.sleep(3)

    driver.save_screenshot('goods_page.png')
    print("✅ Сохранено: goods_page.png")

    # Сохранить HTML
    with open('goods_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("✅ Сохранено: goods_page.html")

    # Попробовать перейти в раздел Продажи
    print("\n💰 Пытаюсь перейти в раздел 'Продажи'...")
    driver.get('https://online.sbis.ru/page/sales')
    time.sleep(3)

    driver.save_screenshot('sales_page.png')
    print("✅ Сохранено: sales_page.png")

    with open('sales_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("✅ Сохранено: sales_page.html")

    print("\n" + "="*60)
    print("✅ Все данные собраны!")
    print("="*60)
    print("Файлы:")
    print("  - main_page.png")
    print("  - goods_page.png + goods_page.html")
    print("  - sales_page.png + sales_page.html")
    print("="*60)

    input("\nНажми Enter чтобы закрыть браузер...")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    driver.save_screenshot('error.png')
    input("\nНажми Enter чтобы закрыть...")

finally:
    driver.quit()
    print("🔒 Браузер закрыт")
