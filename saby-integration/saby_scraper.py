"""
Автоматизация получения данных из Saby Presto через веб-интерфейс
"""

import os
import time
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Загрузить .env
load_dotenv()

class SabyPrestoScraper:
    """Класс для автоматизации работы с Saby Presto"""

    def __init__(self):
        self.email = os.getenv('SABY_EMAIL')
        self.password = os.getenv('SABY_PASSWORD')
        self.driver = None

    def start_browser(self, headless=False):
        """Запустить браузер"""
        print("🚀 Запуск браузера...")

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # Убрать признаки автоматизации
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        if not headless:
            self.driver.maximize_window()

    def login(self):
        """Войти в Saby Presto"""
        print("🔐 Вход в систему...")

        self.driver.get('https://online.sbis.ru')

        # Ждём загрузки страницы
        time.sleep(3)

        try:
            # Сохранить скриншот страницы входа для отладки
            self.driver.save_screenshot('login_page.png')
            print("📸 Скриншот страницы входа: login_page.png")

            # Попробовать разные варианты селекторов
            email_field = None

            # Вариант 1: по name="login"
            try:
                email_field = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "login"))
                )
            except:
                pass

            # Вариант 2: по type="email"
            if not email_field:
                try:
                    email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                except:
                    pass

            # Вариант 3: по placeholder
            if not email_field:
                try:
                    email_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='mail']")
                except:
                    pass

            if not email_field:
                print("❌ Не найдено поле для email")
                print("Проверь скриншот login_page.png")
                return False

            email_field.clear()
            email_field.send_keys(self.email)
            time.sleep(1)

            # Найти поле пароля
            password_field = None
            try:
                password_field = self.driver.find_element(By.NAME, "password")
            except:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                except:
                    pass

            if not password_field:
                print("❌ Не найдено поле для пароля")
                return False

            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(1)

            # Нажать кнопку входа
            login_button = None
            try:
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            except:
                try:
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
                except:
                    pass

            if not login_button:
                print("❌ Не найдена кнопка входа")
                return False

            login_button.click()

            # Ждём загрузки главной страницы
            print("⏳ Ожидание загрузки...")
            time.sleep(7)

            # Проверить что вошли
            current_url = self.driver.current_url
            if 'online.sbis.ru' in current_url and 'auth' not in current_url:
                print("✅ Вход выполнен успешно")
                self.driver.save_screenshot('after_login.png')
                return True
            else:
                print(f"⚠️ Возможно ошибка входа. URL: {current_url}")
                self.driver.save_screenshot('login_error.png')
                return False

        except Exception as e:
            print(f"❌ Ошибка входа: {e}")
            self.driver.save_screenshot('login_exception.png')
            return False

    def get_menu(self):
        """Получить меню"""
        print("📋 Получение меню...")

        try:
            # Перейти в раздел "Товары"
            self.driver.get('https://online.sbis.ru/page/goods')
            time.sleep(3)

            # Здесь нужно будет адаптировать селекторы под реальный интерфейс
            # Пока просто сохраняем HTML страницы
            page_source = self.driver.page_source

            with open('menu_page.html', 'w', encoding='utf-8') as f:
                f.write(page_source)

            print("✅ Страница меню сохранена в menu_page.html")
            print("📸 Делаю скриншот...")

            self.driver.save_screenshot('menu_screenshot.png')
            print("✅ Скриншот сохранён в menu_screenshot.png")

            return True

        except Exception as e:
            print(f"❌ Ошибка получения меню: {e}")
            return False

    def get_sales_data(self):
        """Получить данные о продажах"""
        print("💰 Получение данных о продажах...")

        try:
            # Перейти в раздел "Продажи"
            self.driver.get('https://online.sbis.ru/page/sales')
            time.sleep(3)

            page_source = self.driver.page_source

            with open('sales_page.html', 'w', encoding='utf-8') as f:
                f.write(page_source)

            print("✅ Страница продаж сохранена в sales_page.html")

            self.driver.save_screenshot('sales_screenshot.png')
            print("✅ Скриншот сохранён в sales_screenshot.png")

            return True

        except Exception as e:
            print(f"❌ Ошибка получения продаж: {e}")
            return False

    def close(self):
        """Закрыть браузер"""
        if self.driver:
            self.driver.quit()
            print("🔒 Браузер закрыт")


# === Пример использования ===

if __name__ == "__main__":
    scraper = SabyPrestoScraper()

    try:
        # Запустить браузер (headless=False чтобы видеть что происходит)
        scraper.start_browser(headless=False)

        # Войти
        if scraper.login():
            print("\n" + "="*50)
            print("Успешный вход! Теперь можем получать данные.")
            print("="*50 + "\n")

            # Получить меню
            scraper.get_menu()

            # Получить продажи
            scraper.get_sales_data()

            print("\n✅ Все данные получены!")
            print("Проверь файлы: menu_page.html, sales_page.html")
            print("И скриншоты: menu_screenshot.png, sales_screenshot.png")

        else:
            print("❌ Не удалось войти в систему")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    finally:
        print("\n⏸️  Браузер остаётся открытым 30 секунд для проверки...")
        time.sleep(30)
        scraper.close()
