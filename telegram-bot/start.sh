#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "🤖 Запуск VK-offee Telegram Bot..."

if [[ ! -f ".env" ]]; then
  echo "❌ Файл .env не найден (скопируй .env.example и заполни переменные)"
  exit 1
fi

if [[ -x "venv/bin/python3" ]]; then
  PYTHON_BIN="venv/bin/python3"
else
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" bot.py
