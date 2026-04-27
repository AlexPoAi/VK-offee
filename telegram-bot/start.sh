#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "🤖 Запуск VK-offee Telegram Bot..."

if [[ ! -f ".env" ]]; then
  echo "❌ Файл .env не найден (скопируй .env.example и заполни переменные)"
  exit 1
fi

if [[ "${ALLOW_LOCAL_BOT_RUN:-0}" != "1" ]]; then
  echo "🛑 Локальный запуск product-бота отключён."
  echo "   Канонический runtime: VPS service \`vk-telegram-bot\`."
  echo "   Для локальной отладки запусти так:"
  echo "   ALLOW_LOCAL_BOT_RUN=1 BOT_RUNTIME_MODE=local-debug ./start.sh"
  exit 1
fi

if [[ -x "venv/bin/python3" ]]; then
  PYTHON_BIN="venv/bin/python3"
else
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" bot.py
