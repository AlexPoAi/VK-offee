#!/bin/bash
# Скрипт запуска Telegram бота VK-offee

cd "$(dirname "$0")"

echo "🤖 Запуск VK-offee Telegram Bot..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3."
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
if [ ! -f "venv/.installed" ]; then
    echo "📥 Установка зависимостей..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден. Скопируйте .env.example в .env и настройте."
    exit 1
fi

# Запуск бота
echo "✅ Запуск бота..."
python3 bot.py
