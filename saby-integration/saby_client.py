"""
Saby Presto API Client

Клиент для работы с Saby Presto API через JSON-RPC.
Поддерживает OAuth 2.0 авторизацию и основные операции.
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SabyAPIClient:
    """Клиент для работы с Saby Presto API"""

    BASE_URL = "https://api.sbis.ru"
    AUTH_URL = "https://online.sbis.ru/oauth/service"

    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Инициализация клиента

        Args:
            client_id: ID приложения из личного кабинета Saby
            client_secret: Секретный ключ приложения
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        })

    def authenticate(self) -> bool:
        """
        Получить OAuth токен

        Returns:
            True если авторизация успешна
        """
        if not self.client_id or not self.client_secret:
            raise ValueError("client_id и client_secret обязательны для авторизации")

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            response = self.session.post(self.AUTH_URL, json=payload)
            response.raise_for_status()

            data = response.json()
            self.access_token = data.get('access_token')
            expires_in = data.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })

            return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка авторизации: {e}")
            return False

    def _is_token_valid(self) -> bool:
        """Проверить валидность токена"""
        if not self.access_token or not self.token_expires_at:
            return False
        return datetime.now() < self.token_expires_at

    def _ensure_authenticated(self):
        """Убедиться что токен валиден, иначе обновить"""
        if not self._is_token_valid():
            self.authenticate()

    def _call_method(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Вызвать JSON-RPC метод

        Args:
            method: Название метода API
            params: Параметры метода

        Returns:
            Ответ от API
        """
        self._ensure_authenticated()

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }

        try:
            response = self.session.post(self.BASE_URL, json=payload)
            response.raise_for_status()

            data = response.json()

            if 'error' in data:
                raise Exception(f"API Error: {data['error']}")

            return data.get('result', {})
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            raise

    # === Методы для работы с меню ===

    def get_menu(self) -> Dict[str, Any]:
        """
        Получить меню кофейни

        Returns:
            Словарь с меню (категории, блюда, цены)
        """
        return self._call_method("Presto.GetMenu")

    def get_menu_items(self, category: str = None) -> list:
        """
        Получить позиции меню

        Args:
            category: Фильтр по категории (опционально)

        Returns:
            Список позиций меню
        """
        params = {}
        if category:
            params['category'] = category

        return self._call_method("Presto.GetMenuItems", params)

    # === Методы для работы с ценами ===

    def get_prices(self, item_ids: list = None) -> Dict[str, float]:
        """
        Получить цены на позиции

        Args:
            item_ids: Список ID позиций (если None - все позиции)

        Returns:
            Словарь {item_id: price}
        """
        params = {}
        if item_ids:
            params['item_ids'] = item_ids

        return self._call_method("Retail.GetPrices", params)

    # === Методы для работы с остатками ===

    def get_stock(self, item_ids: list = None) -> Dict[str, float]:
        """
        Получить остатки товаров

        Args:
            item_ids: Список ID товаров (если None - все товары)

        Returns:
            Словарь {item_id: quantity}
        """
        params = {}
        if item_ids:
            params['item_ids'] = item_ids

        return self._call_method("Inventory.GetStock", params)

    # === Методы для работы с продажами ===

    def get_sales_data(self, date_from: str = None, date_to: str = None) -> list:
        """
        Получить данные о продажах

        Args:
            date_from: Дата начала (YYYY-MM-DD)
            date_to: Дата окончания (YYYY-MM-DD)

        Returns:
            Список продаж
        """
        params = {}
        if date_from:
            params['date_from'] = date_from
        if date_to:
            params['date_to'] = date_to

        return self._call_method("Presto.GetSalesData", params)


# === Пример использования ===

if __name__ == "__main__":
    # Инициализация клиента
    client = SabyAPIClient(
        client_id="YOUR_CLIENT_ID",  # Получить из личного кабинета
        client_secret="YOUR_CLIENT_SECRET"
    )

    # Авторизация
    if client.authenticate():
        print("✅ Авторизация успешна")

        # Получить меню
        menu = client.get_menu()
        print(f"Меню: {json.dumps(menu, indent=2, ensure_ascii=False)}")

        # Получить цены
        prices = client.get_prices()
        print(f"Цены: {json.dumps(prices, indent=2, ensure_ascii=False)}")

        # Получить остатки
        stock = client.get_stock()
        print(f"Остатки: {json.dumps(stock, indent=2, ensure_ascii=False)}")
    else:
        print("❌ Ошибка авторизации")
