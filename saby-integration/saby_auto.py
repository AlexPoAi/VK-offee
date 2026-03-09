"""
Автоматический скрипт для Saby Presto
Открывает браузер и ждёт 60 секунд для ручного входа
"""

import time
from selenium import webdriver
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
    print("📖 Открываю https://online.sbis.ru")
    driver.get('https://online.sbis.ru')

    print("\n" + "="*60)
    print("⏸️  У тебя есть 60 секунд для входа:")
    print("="*60)
    print("1. Введи email: vkusnyycoffee@gmail.com")
    print("2. Введи пароль: DD19s8avc55")
    print("3. Нажми 'Войти'")
    print("4. Дождись загрузки главной страницы")
    print("="*60)

    # Ждём 60 секунд
    for i in range(60, 0, -5):
        print(f"⏳ Осталось {i} секунд...")
        time.sleep(5)

    print("\n📸 Делаю скриншоты...")

    # Скриншот текущей страницы
    driver.save_screenshot('current_page.png')
    print("✅ current_page.png")

    # Попробовать перейти в Товары
    print("\n📦 Переход в раздел 'Товары'...")
    driver.get('https://online.sbis.ru/page/goods')
    time.sleep(3)
    driver.save_screenshot('goods_page.png')

    with open('goods_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("✅ goods_page.png + goods_page.html")

    # Попробовать перейти в Продажи
    print("\n💰 Переход в раздел 'Продажи'...")
    driver.get('https://online.sbis.ru/page/sales')
    time.sleep(3)
    driver.save_screenshot('sales_page.png')

    with open('sales_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("✅ sales_page.png + sales_page.html")

    print("\n" + "="*60)
    print("✅ Готово! Файлы сохранены:")
    print("  - current_page.png")
    print("  - goods_page.png + goods_page.html")
    print("  - sales_page.png + sales_page.html")
    print("="*60)

    # Держим браузер открытым ещё 30 секунд
    print("\n⏸️  Браузер останется открытым 30 секунд...")
    time.sleep(30)

except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    driver.save_screenshot('error.png')

finally:
    driver.quit()
    print("🔒 Браузер закрыт")
