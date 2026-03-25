#!/bin/bash
# Запуск VK-телебота (монитор экзокортекса)

cd "$(dirname "$0")"

# Загрузка env
if [ -f "$HOME/.config/aist/env" ]; then
    set -a
    source "$HOME/.config/aist/env"
    set +a
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN не установлен"
    exit 1
fi

echo "🤖 Запуск монитора экзокортекса..."
python3 monitor_bot.py
