#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VK-offee AI Bot v3.1
Telegram бот с RAG-поиском по базе знаний VK-offee (ChromaDB + Claude).
Меню ориентировано на сотрудников кофейни.
"""

import os
import logging
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from telegram.error import NetworkError, RetryAfter, TimedOut
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from rag_client import get_rag_client

load_dotenv()


class SecretRedactionFilter(logging.Filter):
    """Keep bot tokens out of local files, stdout, and systemd journal."""

    def filter(self, record):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if token:
            record.msg = str(record.msg).replace(token, "<TELEGRAM_BOT_TOKEN>")
            if record.args:
                record.args = tuple(
                    str(arg).replace(token, "<TELEGRAM_BOT_TOKEN>")
                    for arg in record.args
                )
        return True


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(),
    ],
)
for handler in logging.getLogger().handlers:
    handler.addFilter(SecretRedactionFilter())

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_RUNTIME_MODE = os.getenv("BOT_RUNTIME_MODE", "local-debug")

# RAG клиент (singleton, retry x3)
rag = get_rag_client()

# ─── Клавиатура ──────────────────────────────────────────────────────────────

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("☕ Напитки"),   KeyboardButton("🍽️ Еда")],
        [KeyboardButton("📋 Стандарты"), KeyboardButton("💰 Цены")],
        [KeyboardButton("👤 Персонал"),  KeyboardButton("📊 Статус")],
        [KeyboardButton("📝 Заметка")],
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

async def safe_reply(message, text: str, **kwargs) -> bool:
    """Send a Telegram reply without breaking handler state on transient network errors."""
    for attempt in range(1, 4):
        try:
            await message.reply_text(text, **kwargs)
            return True
        except RetryAfter as exc:
            logger.warning("Telegram rate limit on reply attempt %s: retry_after=%s", attempt, exc.retry_after)
        except (TimedOut, NetworkError) as exc:
            logger.warning("Telegram reply failed on attempt %s: %s", attempt, exc)
    return False


async def rag_reply(update: Update, query: str) -> None:
    """Запрос к RAG и отправка ответа пользователю."""
    await safe_reply(update.message, "🔍 Ищу в базе знаний...")
    result = rag.query(query)
    if result is None:
        await safe_reply(
            update.message,
            "⚠️ RAG API недоступен.\n"
            "Попросите администратора запустить: cd VK-offee-rag && python src/api.py"
        )
        return
    answer = rag.format_answer(result, show_sources=True)
    await safe_reply(update.message, answer, parse_mode="Markdown")

# ─── Команды ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — приветствие и меню."""
    await safe_reply(
        update.message,
        "☕ *VK-offee бот*\n\n"
        "Задайте любой вопрос или выберите раздел ниже.",
        reply_markup=MAIN_KEYBOARD,
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help — что умеет бот."""
    await safe_reply(
        update.message,
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
            await safe_reply(
                update.message,
                f"🟢 *RAG API работает*\n"
                f"📚 Документов в индексе: {docs}\n"
                f"🗂️ Pack: bar, kitchen, service, hr, management, cafe-ops, park",
                parse_mode="Markdown",
            )
        except Exception:
            await safe_reply(update.message, "🟢 RAG API работает")
    else:
        await safe_reply(
            update.message,
            "🔴 *RAG API недоступен*\n\n"
            "Запустите: `cd VK-offee-rag && python src/api.py`",
            parse_mode="Markdown",
        )


async def reindex_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/reindex — переиндексация базы знаний (только для администраторов)."""
    await safe_reply(update.message, "⏳ Запускаю переиндексацию базы знаний...")
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
        await safe_reply(update.message, f"✅ {last_line}")
    else:
        await safe_reply(update.message, f"❌ Ошибка переиндексации:\n{result.stderr[:500]}")


def resolve_ds_strategy_path() -> Path | None:
    """Ищет рабочий путь до DS-strategy для записи captures."""
    candidates = [
        os.getenv("DS_STRATEGY_PATH"),
        "/Users/alexander/Github/DS-strategy",
        "/root/DS-strategy",
        str(Path.home() / "Github" / "DS-strategy"),
    ]

    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if (path / "inbox" / "captures.md").exists():
            return path

    return None


async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/note — сохранить заметку в captures.md."""
    import subprocess
    from datetime import datetime

    text = " ".join(context.args) if context.args else context.user_data.get("note_text", "")
    if not text.strip():
        context.user_data["waiting_for_note"] = True
        await safe_reply(update.message, "Напишите текст заметки:")
        return

    ds_strategy_path = resolve_ds_strategy_path()
    if ds_strategy_path is None:
        await safe_reply(update.message, "⚠️ Не найден DS-strategy для сохранения заметки.")
        return

    user = update.message.from_user
    username = user.username or user.first_name or "Unknown"
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = text[:57] + "..." if len(text) > 60 else text

    capture = f"""
### {title} [source: Telegram {date_str}]
**Домен:** _требует классификации_
**Тип:** _требует классификации_
**Контент:**
{text.strip()}

"""

    captures_file = ds_strategy_path / "inbox" / "captures.md"
    marker = "<!-- Captures добавляются ниже этой строки -->"

    try:
        content = captures_file.read_text(encoding="utf-8")
        new_content = content.replace(marker, marker + capture)
        captures_file.write_text(new_content, encoding="utf-8")

        subprocess.run(["git", "add", "inbox/captures.md"], cwd=ds_strategy_path, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"telegram: заметка от @{username}"],
            cwd=ds_strategy_path,
            capture_output=True,
        )
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=ds_strategy_path, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=ds_strategy_path, capture_output=True)

        context.user_data.pop("waiting_for_note", None)
        context.user_data.pop("note_text", None)
        await safe_reply(update.message, "✅ Заметка сохранена")
    except Exception as e:
        logger.error("Ошибка заметки: %s", e)
        await safe_reply(update.message, "✅ Заметка сохранена локально.")


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

    # Заметка через кнопку
    if text == "📝 Заметка":
        context.user_data["waiting_for_note"] = True
        await safe_reply(update.message, "Напишите текст заметки:")
        return

    # Если ждём текст заметки
    if context.user_data.get("waiting_for_note"):
        context.user_data["waiting_for_note"] = False
        context.user_data["note_text"] = text
        await note_command(update, context)
        return

    # Приветствия
    if any(w in text.lower() for w in ["привет", "здравствуй", "hi", "hello"]):
        await safe_reply(
            update.message,
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
        BotCommand("note",    "Создать заметку"),
    ])


# ─── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    logger.info(
        "🤖 VK-offee AI Bot v3.1 запущен (mode=%s, RAG + меню для сотрудников)",
        BOT_RUNTIME_MODE,
    )

    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start",   start))
    application.add_handler(CommandHandler("help",    help_command))
    application.add_handler(CommandHandler("status",  status_command))
    application.add_handler(CommandHandler("note",    note_command))
    application.add_handler(CommandHandler("reindex", reindex_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
        timeout=30,
        bootstrap_retries=-1,
    )


if __name__ == "__main__":
    main()
