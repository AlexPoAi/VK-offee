#!/bin/bash
# Guard script: запускает бот в фоновом режиме с защитой от множественных запусков
# Usage: ./guard-bot.sh start|stop|restart|status

set -e

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$BOT_DIR/.bot.pid"
LOGFILE="$BOT_DIR/bot.log"

function is_running() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if kill -0 "$PID" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

function kill_existing() {
    # Kill all existing bot processes (safety measure)
    echo "🔍 Поиск существующих процессов бота..."
    PIDS=$(pgrep -f "python.*bot.py" || true)
    if [ -n "$PIDS" ]; then
        echo "⚠️  Найдены процессы: $PIDS"
        echo "$PIDS" | xargs kill -9 2>/dev/null || true
        echo "✅ Убиты существующие процессы"
        sleep 2
    else
        echo "✅ Существующих процессов не найдено"
    fi
}

function start_bot() {
    if is_running; then
        echo "ℹ️  Бот уже работает (PID: $(cat $PIDFILE))"
        return 0
    fi

    echo "🚀 Запуск бота..."

    # Kill any lingering processes
    kill_existing

    # Start bot in background with nohup
    cd "$BOT_DIR"
    nohup python3 bot.py >> "$LOGFILE" 2>&1 &
    BOT_PID=$!
    echo "$BOT_PID" > "$PIDFILE"

    echo "✅ Бот запущен (PID: $BOT_PID)"
    sleep 2

    # Check if still running
    if kill -0 "$BOT_PID" 2>/dev/null; then
        echo "✅ Бот работает нормально"
        return 0
    else
        echo "❌ Бот упал при запуске! Проверьте логи:"
        tail -20 "$LOGFILE"
        return 1
    fi
}

function stop_bot() {
    if ! is_running; then
        echo "ℹ️  Бот не запущен"
        return 0
    fi

    PID=$(cat "$PIDFILE")
    echo "🛑 Остановка бота (PID: $PID)..."
    kill "$PID" 2>/dev/null || true
    rm -f "$PIDFILE"
    sleep 1
    echo "✅ Бот остановлен"
}

function status_bot() {
    if is_running; then
        PID=$(cat "$PIDFILE")
        echo "🟢 Бот запущен (PID: $PID)"
        ps -p "$PID" -o pid,comm,etime
    else
        echo "🔴 Бот не запущен"
    fi
}

case "${1:-status}" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        stop_bot
        start_bot
        ;;
    status)
        status_bot
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
