#!/bin/bash
# Stage 1 diagnostics for VK-offee Telegram Bot

set -e

echo "════════════════════════════════════════════════════════════════"
echo "🔍 STAGE 1: TELEGRAM BOT & RAG API DIAGNOSTICS"
echo "════════════════════════════════════════════════════════════════"

# Check environment variables
echo ""
echo "1️⃣ Проверка переменных окружения:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f .env ]; then
    echo "✅ .env файл найден"
    TELEGRAM_TOKEN=$(grep "TELEGRAM_BOT_TOKEN" .env | cut -d'=' -f2 | tr -d ' ')
    RAG_API_URL=$(grep "RAG_API_URL" .env | cut -d'=' -f2 | tr -d ' ')
    BOT_RUNTIME_MODE=$(grep "BOT_RUNTIME_MODE" .env | cut -d'=' -f2 | tr -d ' ')

    if [ -z "$TELEGRAM_TOKEN" ]; then
        echo "❌ TELEGRAM_BOT_TOKEN не установлен"
    else
        echo "✅ TELEGRAM_BOT_TOKEN установлен (${#TELEGRAM_TOKEN} chars)"
    fi

    if [ -z "$RAG_API_URL" ]; then
        echo "⚠️  RAG_API_URL не установлен, fallback: http://127.0.0.1:8000"
    else
        echo "✅ RAG_API_URL = $RAG_API_URL"
    fi

    echo "✅ BOT_RUNTIME_MODE = ${BOT_RUNTIME_MODE:-local-debug}"
else
    echo "❌ .env файл не найден!"
    exit 1
fi

# Check RAG API health
echo ""
echo "2️⃣ Проверка RAG API доступности:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

RAG_URL="${RAG_API_URL:-http://127.0.0.1:8000}"

if curl -s --connect-timeout 3 "$RAG_URL/health" > /dev/null 2>&1; then
    echo "✅ RAG API доступен на: $RAG_URL"
    HEALTH_DATA=$(curl -s "$RAG_URL/health")
    DOCS=$(echo "$HEALTH_DATA" | grep -o '"documents_indexed":[0-9]*' | cut -d':' -f2)
    echo "   📚 Документов в индексе: $DOCS"
else
    echo "❌ RAG API недоступен на: $RAG_URL"
    echo "   Попыточка localhost:"
    if curl -s --connect-timeout 3 "http://127.0.0.1:8000/health" > /dev/null 2>&1; then
        echo "   ✅ Найден на localhost:8000"
        echo "   💡 Совет: запустить RAG локально или обновить RAG_API_URL"
    else
        echo "   ❌ RAG API недоступен ни на одном адресе"
    fi
fi

# Test RAG query
echo ""
echo "3️⃣ Проверка RAG query endpoint:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

RESPONSE=$(curl -s -X POST "$RAG_URL/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"Как приготовить капучино?","n_results":2}' 2>&1)

if echo "$RESPONSE" | grep -q '"answer"'; then
    echo "✅ RAG /query endpoint работает"
    SOURCES=$(echo "$RESPONSE" | grep -o '"pack"' | wc -l)
    echo "   📦 Вернулось источников: $SOURCES"
else
    echo "❌ RAG /query endpoint не работает или возвращает ошибку"
    echo "   Ответ: $(echo "$RESPONSE" | head -c 100)..."
fi

# Check Python dependencies
echo ""
echo "4️⃣ Проверка Python зависимостей:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 -c "import telegram; print('✅ python-telegram-bot: OK')" 2>/dev/null || echo "❌ python-telegram-bot: НЕ УСТАНОВЛЕН"
python3 -c "import dotenv; print('✅ python-dotenv: OK')" 2>/dev/null || echo "❌ python-dotenv: НЕ УСТАНОВЛЕН"
python3 -c "import requests; print('✅ requests: OK')" 2>/dev/null || echo "❌ requests: НЕ УСТАНОВЛЕН"

# Check bot process
echo ""
echo "5️⃣ Проверка процесса бота:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if pgrep -f "python.*bot.py" > /dev/null; then
    echo "🟢 Бот запущен (PID: $(pgrep -f 'python.*bot.py'))"
else
    echo "🔴 Бот НЕ запущен"
    echo "   💡 Запуск: python3 bot.py"
fi

# Check bot.log
echo ""
echo "6️⃣ Последние ошибки в логе (если есть):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f bot.log ]; then
    echo "📋 bot.log (последние 10 строк):"
    tail -10 bot.log | sed 's/^/   /'
else
    echo "⚠️  bot.log не найден"
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📊 РЕЗУЛЬТАТЫ ДИАГНОСТИКИ"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ Готово. Следующий шаг: Stage 2 — исправления кода"
echo ""
