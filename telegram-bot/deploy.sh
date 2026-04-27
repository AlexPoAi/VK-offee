#!/bin/bash
# deploy.sh — разворачивает VK-offee бот + RAG API на Ubuntu 22.04
# Использование: bash deploy.sh
set -e

echo "🚀 VK-offee Bot Deploy — старт"
echo "================================"

# === 1. Системные зависимости ===
echo ""
echo "[1/7] Обновление системы и установка зависимостей..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip git curl

# === 2. Создаём рабочую директорию ===
echo ""
echo "[2/7] Создание рабочей директории /opt/vk-offee..."
mkdir -p /opt/vk-offee
cd /opt/vk-offee

# === 3. Клонируем репозитории ===
echo ""
echo "[3/7] Клонирование репозиториев..."

if [ -d "VK-offee" ]; then
    echo "  VK-offee уже есть — обновляем..."
    git -C VK-offee pull
else
    git clone https://github.com/AlexPoAi/VK-offee.git
fi

if [ -d "VK-offee-rag" ]; then
    echo "  VK-offee-rag уже есть — обновляем..."
    git -C VK-offee-rag pull
else
    git clone https://github.com/AlexPoAi/VK-offee-rag.git
fi

# === 4. Python окружения ===
echo ""
echo "[4/7] Установка Python зависимостей..."

# RAG API
cd /opt/vk-offee/VK-offee-rag
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q fastapi uvicorn chromadb openai anthropic python-dotenv
deactivate

# Telegram бот
cd /opt/vk-offee/VK-offee/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q python-telegram-bot python-dotenv requests tenacity
deactivate

# === 5. .env файлы ===
echo ""
echo "[5/7] Настройка переменных окружения..."

# RAG API .env
if [ ! -f /opt/vk-offee/VK-offee-rag/.env ]; then
    cat > /opt/vk-offee/VK-offee-rag/.env << 'ENVFILE'
ANTHROPIC_API_KEY=ВСТАВЬ_СЮДА
OPENAI_API_KEY=ВСТАВЬ_СЮДА
PACK_PATH=/opt/vk-offee/VK-offee
CHROMA_PATH=/opt/vk-offee/VK-offee-rag/data/chroma
API_HOST=127.0.0.1
API_PORT=8000
ENVFILE
    echo "  ⚠️  Заполни /opt/vk-offee/VK-offee-rag/.env"
fi

# Telegram бот .env
if [ ! -f /opt/vk-offee/VK-offee/telegram-bot/.env ]; then
    cat > /opt/vk-offee/VK-offee/telegram-bot/.env << 'ENVFILE'
TELEGRAM_BOT_TOKEN=ВСТАВЬ_СЮДА
WAREHOUSE_REPORT_CHAT_ID=ВСТАВЬ_СЮДА
# или TELEGRAM_CHAT_ID=ВСТАВЬ_СЮДА
RAG_API_URL=http://127.0.0.1:8000
RAG_TIMEOUT=30
BOT_RUNTIME_MODE=cloud
TELEGRAM_ALLOWED_CHAT_ID=
TELEGRAM_TASK_INBOX=/opt/vk-offee/VK-offee/telegram-bot/inbox
CODEX_RUNTIME_ROOT=/opt/vk-offee/VK-offee/PACK-codex-runtime/runtime
ENVFILE
    echo "  ⚠️  Заполни /opt/vk-offee/VK-offee/telegram-bot/.env"
fi

# === 6. Systemd сервисы ===
echo ""
echo "[6/7] Регистрация systemd сервисов..."

# RAG API сервис
cat > /etc/systemd/system/vk-rag-api.service << 'SERVICE'
[Unit]
Description=VK-offee RAG API
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/vk-offee/VK-offee-rag
ExecStartPre=/opt/vk-offee/VK-offee-rag/venv/bin/python3 src/indexer.py --pack-path /opt/vk-offee/VK-offee --chroma-path /opt/vk-offee/VK-offee-rag/data/chroma
ExecStart=/opt/vk-offee/VK-offee-rag/venv/bin/python3 src/api.py
Restart=always
RestartSec=10
EnvironmentFile=/opt/vk-offee/VK-offee-rag/.env

[Install]
WantedBy=multi-user.target
SERVICE

# Telegram бот сервис
cat > /etc/systemd/system/vk-telegram-bot.service << 'SERVICE'
[Unit]
Description=VK-offee Telegram Bot
After=network.target vk-rag-api.service
Wants=vk-rag-api.service

[Service]
Type=simple
WorkingDirectory=/opt/vk-offee/VK-offee/telegram-bot
ExecStart=/opt/vk-offee/VK-offee/telegram-bot/venv/bin/python3 bot.py
Restart=always
RestartSec=10
EnvironmentFile=/opt/vk-offee/VK-offee/telegram-bot/.env

[Install]
WantedBy=multi-user.target
SERVICE

# RAG reindex timer
cat > /etc/systemd/system/vk-rag-reindex.service << 'SERVICE'
[Unit]
Description=VK-offee RAG reindex if Pack changed
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/opt/vk-offee/VK-offee-rag
ExecStart=/opt/vk-offee/VK-offee-rag/scripts/reindex-if-pack-changed.sh
SERVICE

cat > /etc/systemd/system/vk-rag-reindex.timer << 'SERVICE'
[Unit]
Description=Periodic VK-offee Pack sync and RAG reindex

[Timer]
OnBootSec=3min
OnUnitActiveSec=10min
Unit=vk-rag-reindex.service
Persistent=true

[Install]
WantedBy=timers.target
SERVICE

chmod +x /opt/vk-offee/VK-offee-rag/scripts/reindex-if-pack-changed.sh

systemctl daemon-reload
systemctl enable vk-rag-api vk-telegram-bot vk-rag-reindex.timer
echo "  ✅ Сервисы и timer зарегистрированы"

# === 7. Итог ===
echo ""
echo "================================"
echo "✅ Deploy завершён!"
echo ""
echo "⚠️  ВАЖНО — заполни токены:"
echo "   nano /opt/vk-offee/VK-offee-rag/.env"
echo "   nano /opt/vk-offee/VK-offee/telegram-bot/.env"
echo ""
echo "Затем запусти сервисы:"
echo "   systemctl start vk-rag-api"
echo "   systemctl start vk-telegram-bot"
echo "   systemctl start vk-rag-reindex.timer"
echo ""
echo "Проверка статуса:"
echo "   systemctl status vk-rag-api"
echo "   systemctl status vk-telegram-bot"
echo "   systemctl status vk-rag-reindex.timer"
echo ""
echo "Логи:"
echo "   journalctl -u vk-rag-api -f"
echo "   journalctl -u vk-telegram-bot -f"
echo "   journalctl -u vk-rag-reindex.service -f"
