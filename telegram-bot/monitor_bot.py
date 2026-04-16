#!/usr/bin/env python3
"""
VK-телебот: монитор экзокортекса
Команды: /status, /agents, /wp, /logs
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Пути
HOME = Path.home()
STRATEGY_DIR = HOME / "Github" / "DS-strategy"
STATUS_DIR = HOME / ".local" / "state" / "exocortex" / "status"
LOGS_DIR = HOME / "logs"

# Env
TOKEN = os.getenv("MONITOR_BOT_TOKEN")
if not TOKEN:
    print("ERROR: MONITOR_BOT_TOKEN not set")
    sys.exit(1)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статус всех агентов"""
    status_file = STRATEGY_DIR / "current" / "AGENTS-STATUS.md"

    if not status_file.exists():
        await update.message.reply_text("❌ Файл статуса не найден")
        return

    content = status_file.read_text()
    lines = content.split('\n')

    # Извлекаем ключевые строки
    brain_line = next((l for l in lines if 'Мозг экзокортекса' in l), "")
    tasks_section = []
    in_tasks = False

    for line in lines:
        if '## Задачи' in line:
            in_tasks = True
            continue
        if in_tasks and line.startswith('- '):
            tasks_section.append(line)

    message = f"<b>🧠 Статус экзокортекса</b>\n\n"
    message += f"{brain_line}\n\n"
    message += "<b>Задачи:</b>\n"
    message += "\n".join(tasks_section[:6])

    await update.message.reply_text(message, parse_mode='HTML')


async def agents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Список агентов и последний запуск"""
    agents = []

    if STATUS_DIR.exists():
        for status_file in STATUS_DIR.glob("*.status"):
            name = status_file.stem
            mtime = datetime.fromtimestamp(status_file.stat().st_mtime)
            agents.append((name, mtime))

    agents.sort(key=lambda x: x[1], reverse=True)

    message = "<b>🤖 Агенты экзокортекса</b>\n\n"

    for name, mtime in agents[:10]:
        time_str = mtime.strftime("%d.%m %H:%M")
        message += f"• {name}: {time_str}\n"

    if not agents:
        message += "Нет данных о запусках"

    await update.message.reply_text(message, parse_mode='HTML')


async def wp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Активные РП текущей недели"""
    week_files = list(STRATEGY_DIR.glob("current/WeekPlan*.md"))

    if not week_files:
        await update.message.reply_text("❌ WeekPlan не найден")
        return

    latest = max(week_files, key=lambda f: f.stat().st_mtime)
    content = latest.read_text()

    lines = content.split('\n')
    wp_lines = [l for l in lines if l.startswith('| ') and 'pending' in l or 'in_progress' in l]

    message = f"<b>📋 Активные РП</b>\n\n"

    for line in wp_lines[:10]:
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 3:
            message += f"• {parts[1]} ({parts[3]})\n"

    if not wp_lines:
        message += "Нет активных РП"

    await update.message.reply_text(message, parse_mode='HTML')


async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Последние ошибки из логов"""
    today = datetime.now().strftime("%Y-%m-%d")
    errors = []

    for agent in ['strategist', 'extractor', 'synchronizer']:
        log_file = LOGS_DIR / agent / f"{today}.log"
        if log_file.exists():
            content = log_file.read_text()
            error_lines = [l for l in content.split('\n') if 'ERROR' in l or 'CRITICAL' in l]
            errors.extend([(agent, l) for l in error_lines[-3:]])

    message = "<b>🚨 Последние ошибки</b>\n\n"

    if errors:
        for agent, line in errors[-10:]:
            message += f"<b>{agent}:</b> {line[:100]}\n\n"
    else:
        message += "✅ Ошибок не обнаружено"

    await update.message.reply_text(message, parse_mode='HTML')


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("agents", agents_command))
    app.add_handler(CommandHandler("wp", wp_command))
    app.add_handler(CommandHandler("logs", logs_command))

    print("🤖 VK-телебот запущен (монитор экзокортекса)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
