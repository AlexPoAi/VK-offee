#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VK-offee AI Bot v3.1
Telegram бот с RAG-поиском по базе знаний VK-offee (ChromaDB + Claude).
Меню ориентировано на сотрудников кофейни.
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from rag_client import get_rag_client

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# RAG клиент (singleton, retry x3)
rag = get_rag_client()

# ─── Клавиатура ──────────────────────────────────────────────────────────────

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("☕ Напитки"),   KeyboardButton("🍽️ Еда")],
        [KeyboardButton("📋 Стандарты"), KeyboardButton("💰 Цены")],
        [KeyboardButton("👤 Персонал"),  KeyboardButton("📊 Статус")],
    ],
    resize_keyboard=True,
)

# Быстрые RAG-запросы для каждой кнопки
BUTTON_QUERIES = {
    "☕ Напитки":    "Список напитков и рецептуры бара VK-offee",
    "🍽️ Еда":        "Список блюд и заготовки кухни VK-offee",
    "📋 Стандарты":  "Стандарты обслуживания и чек-листы смены",
    "💰 Цены":       "Прайс-лист напитков и еды VK-offee",
    "👤 Персонал":   "Ставки оплаты труда бариста официант повар раннер",
}

# ─── Хелпер ──────────────────────────────────────────────────────────────────

async def rag_reply(update: Update, query: str) -> None:
    """Запрос к RAG и отправка ответа пользователю."""
    await update.message.reply_text("🔍 Ищу в базе знаний...")
    result = rag.query(query)
    if result is None:
        await update.message.reply_text(
            "⚠️ RAG API недоступен.\n"
            "Попросите администратора запустить: cd VK-offee-rag && python src/api.py"
        )
        return
    answer = rag.format_answer(result, show_sources=True)
    await update.message.reply_text(answer, parse_mode="Markdown")

# ─── Команды ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — приветствие и меню."""
    await update.message.reply_text(
        "☕ *VK-offee бот*\n\n"
        "Задайте любой вопрос или выберите раздел ниже.",
        reply_markup=MAIN_KEYBOARD,
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help — что умеет бот."""
    await update.message.reply_text(
        "📚 *Что умею:*\n\n"
        "• Отвечать на любые вопросы по базе знаний кофейни\n"
        "• Показывать рецептуры напитков и блюд\n"
        "• Показывать прайс-лист и ставки персонала\n"
        "• Находить стандарты обслуживания и чек-листы\n\n"
        "Просто напишите вопрос — например:\n"
        "_«Как приготовить капучино?»_\n"
        "_«Состав боула с индейкой»_\n"
        "_«Ставка бариста»_",
        parse_mode="Markdown",
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/status — проверка RAG API и индекса."""
    available = rag.is_available()
    if available:
        # Получаем количество документов из health endpoint
        import requests
        try:
            data = requests.get("http://127.0.0.1:8000/health", timeout=5).json()
            docs = data.get("documents_indexed", "?")
            await update.message.reply_text(
                f"🟢 *RAG API работает*\n"
                f"📚 Документов в индексе: {docs}\n"
                f"🗂️ Pack: bar, kitchen, service, hr, management, cafe-ops, park",
                parse_mode="Markdown",
            )
        except Exception:
            await update.message.reply_text("🟢 RAG API работает")
    else:
        await update.message.reply_text(
            "🔴 *RAG API недоступен*\n\n"
            "Запустите: `cd VK-offee-rag && python src/api.py`",
            parse_mode="Markdown",
        )


async def reindex_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/reindex — переиндексация базы знаний (только для администраторов)."""
    await update.message.reply_text("⏳ Запускаю переиндексацию базы знаний...")
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "src/indexer.py",
         "--pack-path", "/Users/alexander/Github/VK-offee",
         "--chroma-path", "./data/chroma",
         "--reset"],
        capture_output=True, text=True,
        cwd="/Users/alexander/Github/VK-offee-rag",
    )
    if result.returncode == 0:
        # Последняя строка содержит итог
        last_line = [l for l in result.stdout.strip().split("\n") if l][-1]
        await update.message.reply_text(f"✅ {last_line}")
    else:
        await update.message.reply_text(f"❌ Ошибка переиндексации:\n{result.stderr[:500]}")


# ─── Обработчик сообщений ─────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Текстовые сообщения: кнопки меню или свободный вопрос → RAG."""
    text = update.message.text

    # Кнопки меню → предустановленный RAG-запрос
    if text in BUTTON_QUERIES:
        await rag_reply(update, BUTTON_QUERIES[text])
        return

    # Статус через кнопку
    if text == "📊 Статус":
        await status_command(update, context)
        return

    # Приветствия
    if any(w in text.lower() for w in ["привет", "здравствуй", "hi", "hello"]):
        await update.message.reply_text(
            "Привет! 👋 Задайте вопрос по базе знаний кофейни.",
            reply_markup=MAIN_KEYBOARD,
        )
        return

    # Любой свободный вопрос → RAG
    await rag_reply(update, text)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error: %s", update, context.error)


# ─── Регистрация команд в BotFather ──────────────────────────────────────────

async def post_init(application: Application) -> None:
    """Регистрирует команды в Telegram (показываются в меню /commands)."""
    await application.bot.set_my_commands([
        BotCommand("start",   "Главное меню"),
        BotCommand("help",    "Что умеет бот"),
        BotCommand("status",  "Статус RAG API и индекса"),
        BotCommand("reindex", "Переиндексировать базу знаний"),
    ])


# ─── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    logger.info("🤖 VK-offee AI Bot v3.1 запущен (RAG + меню для сотрудников)")

    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start",   start))
    application.add_handler(CommandHandler("help",    help_command))
    application.add_handler(CommandHandler("status",  status_command))
    application.add_handler(CommandHandler("reindex", reindex_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
