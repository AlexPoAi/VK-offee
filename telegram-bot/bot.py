#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VK-offee AI Bot v3.1
Telegram бот с RAG-поиском по базе знаний VK-offee.
Меню ориентировано на сотрудников кофейни и отдельный Codex runtime.
"""

import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import BotCommand, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.error import NetworkError, RetryAfter, TimedOut
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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
ALLOWED_CHAT_ID = str(os.getenv("TELEGRAM_ALLOWED_CHAT_ID") or os.getenv("TELEGRAM_CHAT_ID") or "").strip()
TASK_INBOX = Path(
    os.getenv("TELEGRAM_TASK_INBOX")
    or (Path(__file__).resolve().parent / "inbox")
)
CODEX_RUNTIME_ROOT = Path(
    os.getenv("CODEX_RUNTIME_ROOT")
    or (Path(__file__).resolve().parents[1] / "PACK-codex-runtime" / "runtime")
)
CODEX_SESSIONS_DIR = CODEX_RUNTIME_ROOT / "sessions"
CODEX_TASKS_DIR = CODEX_RUNTIME_ROOT / "tasks"
CODEX_ARTIFACTS_DIR = CODEX_RUNTIME_ROOT / "artifacts"
CODEX_MEMORY_DIR = CODEX_RUNTIME_ROOT / "memory"
CODEX_OUTBOX_DIR = CODEX_RUNTIME_ROOT / "outbox"
CODEX_REGISTRY_DIR = CODEX_RUNTIME_ROOT / "registry"
CODEX_ACTIVE_SESSIONS_FILE = CODEX_REGISTRY_DIR / "active-sessions.json"

for runtime_dir in (
    CODEX_SESSIONS_DIR,
    CODEX_TASKS_DIR,
    CODEX_ARTIFACTS_DIR,
    CODEX_MEMORY_DIR,
    CODEX_OUTBOX_DIR,
    CODEX_REGISTRY_DIR,
):
    runtime_dir.mkdir(parents=True, exist_ok=True)

# RAG клиент (singleton, retry x3)
rag = get_rag_client()


def resolve_rag_repo_path() -> Path | None:
    """Ищет рабочий путь до VK-offee-rag для reindex/debug hints."""
    candidates = [
        os.getenv("VKOFFEE_RAG_PATH"),
        "/Users/alexander/Github/VK-offee-rag",
        "/opt/vk-offee/VK-offee-rag",
        str(Path(__file__).resolve().parents[2] / "VK-offee-rag"),
    ]

    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if (path / "src" / "api.py").exists():
            return path
    return None


def rag_start_hint() -> str:
    rag_repo = resolve_rag_repo_path()
    if rag_repo:
        return f"cd {rag_repo} && python src/api.py"
    return "cd VK-offee-rag && python src/api.py"


# ─── Клавиатура ──────────────────────────────────────────────────────────────

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("☕ Напитки"), KeyboardButton("🍽️ Еда")],
        [KeyboardButton("📋 Стандарты"), KeyboardButton("💰 Цены")],
        [KeyboardButton("👤 Персонал"), KeyboardButton("📊 Статус")],
        [KeyboardButton("🤖 Codex"), KeyboardButton("📚 База знаний")],
        [KeyboardButton("📝 Заметка"), KeyboardButton("🧠 Задача")],
        [KeyboardButton("🎨 Дизайн")],
    ],
    resize_keyboard=True,
)

BUTTON_QUERIES = {
    "☕ Напитки": "Список напитков и рецептуры бара VK-offee",
    "🍽️ Еда": "Список блюд и заготовки кухни VK-offee",
    "📋 Стандарты": "Стандарты обслуживания и чек-листы смены",
    "💰 Цены": "Прайс-лист напитков и еды VK-offee",
    "👤 Персонал": "Ставки оплаты труда бариста официант повар раннер",
}

TASK_KIND_LABELS = {
    "task": "общая задача",
    "design": "дизайн-задача",
    "codex": "codex-задача",
}


# ─── Хелперы ─────────────────────────────────────────────────────────────────

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


def is_authorized_chat(update: Update) -> bool:
    """Проверяет, что приватные task/design-функции вызваны из разрешённого чата."""
    if not ALLOWED_CHAT_ID:
        return True
    chat = update.effective_chat
    return bool(chat and str(chat.id) == ALLOWED_CHAT_ID)


async def require_authorized_chat(update: Update) -> bool:
    """Мягко отказывает, если команда пришла не из доверенного личного чата."""
    if is_authorized_chat(update):
        return True
    if update.message:
        await safe_reply(update.message, "⛔ Эта функция доступна только в доверенном личном чате.")
    return False


def reset_intake_state(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("waiting_for_task_kind", None)


def set_chat_mode(context: ContextTypes.DEFAULT_TYPE, mode: str) -> None:
    context.user_data["chat_mode"] = mode


def get_chat_mode(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("chat_mode", "rag")


def build_inbox_paths(kind: str) -> tuple[Path, str]:
    now = datetime.now()
    date_dir = TASK_INBOX / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%H%M%S")
    return date_dir, stamp


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_active_sessions() -> dict[str, str]:
    if not CODEX_ACTIVE_SESSIONS_FILE.exists():
        return {}
    try:
        return json.loads(CODEX_ACTIVE_SESSIONS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("active-sessions registry is corrupted, resetting")
        return {}


def save_active_sessions(data: dict[str, str]) -> None:
    CODEX_ACTIVE_SESSIONS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_codex_session_card(session_id: str, chat_id: str, username: str) -> str:
    opened = now_str()
    return f"""---
type: session-card
session_id: {session_id}
channel: telegram
chat_id: "{chat_id}"
thread_key: "{chat_id}"
status: active
opened_at: {opened}
last_activity_at: {opened}
active_task_id: ""
owner_role: Session Operator
---

# Session `{session_id}`

## Назначение

Живая Telegram-сессия пользователя @{username or "telegram-user"} в режиме `Codex`.

## Контекст

- канал: `telegram`
- инициатор: @{username or "telegram-user"}
- режим: `Codex mode`

## Active Tasks

- пока нет

## Related Artifacts

- пока нет

## Current State

- `accepted`

## Last Truthful Summary

Сессия открыта. Ожидает первую или следующую задачу.
"""


def create_codex_session(chat_id: str, username: str) -> tuple[str, Path]:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    session_id = f"CODEX.SESSION.{stamp}"
    path = CODEX_SESSIONS_DIR / f"{session_id}.md"
    path.write_text(build_codex_session_card(session_id, chat_id, username), encoding="utf-8")

    active_sessions = load_active_sessions()
    active_sessions[chat_id] = session_id
    save_active_sessions(active_sessions)
    return session_id, path


def get_or_create_codex_session(chat_id: str, username: str) -> tuple[str, Path, bool]:
    active_sessions = load_active_sessions()
    session_id = active_sessions.get(chat_id, "").strip()
    if session_id:
        session_path = CODEX_SESSIONS_DIR / f"{session_id}.md"
        if session_path.exists():
            return session_id, session_path, False
    session_id, session_path = create_codex_session(chat_id, username)
    return session_id, session_path, True


def update_session_card(session_path: Path, task_id: str, summary: str) -> None:
    content = session_path.read_text(encoding="utf-8")
    replacements = {
        "last_activity_at: ": f"last_activity_at: {now_str()}",
        'active_task_id: ""': f'active_task_id: "{task_id}"',
    }
    for needle, replacement in replacements.items():
        if needle in content:
            if needle == "last_activity_at: ":
                lines = []
                for line in content.splitlines():
                    if line.startswith("last_activity_at: "):
                        lines.append(replacement)
                    else:
                        lines.append(line)
                content = "\n".join(lines)
            else:
                content = content.replace(needle, replacement, 1)
    if "## Last Truthful Summary" in content:
        head, _, _tail = content.partition("## Last Truthful Summary")
        content = head + "## Last Truthful Summary\n\n" + summary.strip() + "\n"
    session_path.write_text(content, encoding="utf-8")


def materialize_codex_task(
    session_id: str,
    kind: str,
    username: str,
    text: str,
    source_message_id: str,
    attachments: list[str] | None = None,
) -> tuple[str, Path]:
    attachments = attachments or []
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    task_id = f"CODEX.TASK.{stamp}"
    task_path = CODEX_TASKS_DIR / f"{task_id}.md"
    attachments_block = "\n".join(f"- `{name}`" for name in attachments) if attachments else "- нет вложений"
    task_path.write_text(
        f"""---
type: task-card
task_id: {task_id}
session_id: {session_id}
kind: {kind}
channel: telegram
source_message_id: "{source_message_id}"
status: accepted
created_at: {now_str()}
updated_at: {now_str()}
owner_role: Codex Agent
---

# Task `{task_id}`

## Вход

{text.strip() if text.strip() else "_без текста_"}

## Attachments

{attachments_block}

## Domain Routing

- `PACK-codex-runtime`

## Processing State

- `accepted`

## Result

Задача принята в Codex runtime. Ожидает обработки.
""",
        encoding="utf-8",
    )
    return task_id, task_path


def persist_task_markdown(kind: str, username: str, text: str, attachments: list[str] | None = None) -> Path:
    date_dir, stamp = build_inbox_paths(kind)
    path = date_dir / f"{stamp}-{kind}.md"
    attachments = attachments or []

    lines = [
        f"# Telegram {TASK_KIND_LABELS.get(kind, kind)}",
        "",
        f"- `kind`: {kind}",
        f"- `created_at`: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "- `source`: telegram",
        f"- `from`: @{username}" if username else "- `from`: telegram-user",
        "",
        "## Сообщение",
        "",
        text.strip() if text.strip() else "_без текста_",
        "",
    ]

    if attachments:
        lines.extend(["## Вложения", ""])
        for attachment in attachments:
            lines.append(f"- `{attachment}`")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


async def save_photo_task(update: Update, context: ContextTypes.DEFAULT_TYPE, kind: str) -> Path:
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    date_dir, stamp = build_inbox_paths(kind)
    photo_path = date_dir / f"{stamp}-{kind}.jpg"
    await file.download_to_drive(custom_path=str(photo_path))
    return photo_path


async def save_codex_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, task_id: str) -> Path:
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    artifact_path = CODEX_ARTIFACTS_DIR / f"{task_id}.jpg"
    await file.download_to_drive(custom_path=str(artifact_path))
    return artifact_path


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.warning(
            "Git command failed: %s\nstdout=%s\nstderr=%s",
            " ".join(args),
            result.stdout.strip(),
            result.stderr.strip(),
        )
    return result


def resolve_ds_strategy_path() -> Path | None:
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


# ─── RAG команды ─────────────────────────────────────────────────────────────

async def rag_reply(update: Update, query: str) -> None:
    await safe_reply(update.message, "🔍 Ищу в базе знаний...")
    result = rag.query(query)
    if result is None:
        await safe_reply(
            update.message,
            "⚠️ RAG API недоступен.\n"
            f"Текущий endpoint: `{rag.base_url}`\n"
            f"Запуск: `{rag_start_hint()}`",
            parse_mode="Markdown",
        )
        return
    answer = rag.format_answer(result, show_sources=True)
    await safe_reply(update.message, answer, parse_mode="Markdown")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await safe_reply(
        update.message,
        "☕ *VK-offee бот*\n\n"
        "Задайте любой вопрос или выберите раздел ниже.",
        reply_markup=MAIN_KEYBOARD,
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await safe_reply(
        update.message,
        "📚 *Что умею:*\n\n"
        "• Отвечать на любые вопросы по базе знаний кофейни\n"
        "• Показывать рецептуры напитков и блюд\n"
        "• Показывать прайс-лист и ставки персонала\n"
        "• Находить стандарты обслуживания и чек-листы\n\n"
        "Отдельно есть режим `🤖 Codex` для задач, фото и рабочих запросов вне RAG.\n\n"
        "Просто напишите вопрос — например:\n"
        "_«Как приготовить капучино?»_\n"
        "_«Состав боула с индейкой»_\n"
        "_«Ставка бариста»_",
        parse_mode="Markdown",
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = rag.health()
    if data:
        docs = data.get("documents_indexed", "?")
        await safe_reply(
            update.message,
            f"🟢 *RAG API работает*\n"
            f"🌐 Endpoint: `{rag.base_url}`\n"
            f"📚 Документов в индексе: {docs}\n"
            f"🗂️ Pack: bar, kitchen, service, hr, management, cafe-ops, park",
            parse_mode="Markdown",
        )
        return

    await safe_reply(
        update.message,
        "🔴 *RAG API недоступен*\n\n"
        f"Endpoint: `{rag.base_url}`\n"
        f"Запуск: `{rag_start_hint()}`",
        parse_mode="Markdown",
    )


async def reindex_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await safe_reply(update.message, "⏳ Запускаю переиндексацию базы знаний...")
    import sys

    rag_repo = resolve_rag_repo_path()
    if rag_repo is None:
        await safe_reply(update.message, "❌ Не найден VK-offee-rag для переиндексации.")
        return

    pack_path = Path(os.getenv("VKOFFEE_PACK_PATH") or Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "src/indexer.py",
            "--pack-path",
            str(pack_path),
            "--chroma-path",
            "./data/chroma",
            "--reset",
        ],
        capture_output=True,
        text=True,
        cwd=rag_repo,
    )
    if result.returncode == 0:
        last_line = [line for line in result.stdout.strip().split("\n") if line][-1]
        await safe_reply(update.message, f"✅ {last_line}")
    else:
        await safe_reply(update.message, f"❌ Ошибка переиндексации:\n{result.stderr[:500]}")


async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args) if context.args else context.user_data.get("note_text", "")
    note_text = text.strip()
    if not note_text:
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
    title = note_text[:57] + "..." if len(note_text) > 60 else note_text

    capture = f"""
### {title} [source: Telegram {date_str}]
**Домен:** _требует классификации_
**Тип:** _требует классификации_
**Контент:**
{note_text}

"""

    captures_file = ds_strategy_path / "inbox" / "captures.md"
    marker = "<!-- Captures добавляются ниже этой строки -->"

    try:
        run_git(["git", "pull", "--rebase", "--autostash", "origin", "main"], ds_strategy_path)
        content = captures_file.read_text(encoding="utf-8")
        if f"**Контент:**\n{note_text}\n" in content:
            context.user_data.pop("waiting_for_note", None)
            context.user_data.pop("note_text", None)
            await safe_reply(update.message, "✅ Заметка уже сохранена")
            return

        if marker in content:
            new_content = content.replace(marker, marker + capture)
        else:
            new_content = content.rstrip() + "\n" + capture

        captures_file.write_text(new_content, encoding="utf-8")
        run_git(["git", "add", "inbox/captures.md"], ds_strategy_path)
        commit_result = run_git(
            ["git", "commit", "-m", f"telegram: заметка от @{username}"],
            ds_strategy_path,
        )
        commit_output = f"{commit_result.stdout}\n{commit_result.stderr}"
        if commit_result.returncode == 0 or "nothing to commit" in commit_output:
            run_git(["git", "pull", "--rebase", "--autostash", "origin", "main"], ds_strategy_path)
            run_git(["git", "push", "origin", "main"], ds_strategy_path)

        context.user_data.pop("waiting_for_note", None)
        context.user_data.pop("note_text", None)
        await safe_reply(update.message, "✅ Заметка сохранена")
    except Exception as error:
        logger.error("Ошибка заметки: %s", error)
        await safe_reply(update.message, "✅ Заметка сохранена локально.")


async def task_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_authorized_chat(update):
        return

    text = " ".join(context.args).strip()
    if text:
        username = update.effective_user.username or update.effective_user.first_name or "Unknown"
        path = persist_task_markdown("task", username, text)
        await safe_reply(
            update.message,
            f"✅ Задача принята и сохранена в inbox.\n`{path.name}`",
            parse_mode="Markdown",
        )
        return

    context.user_data["waiting_for_task_kind"] = "task"
    await safe_reply(
        update.message,
        "Напиши текст задачи или пришли фото следующим сообщением.\n"
        "Я сохраню это как входящую задачу для обработки.",
    )


async def design_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_authorized_chat(update):
        return

    text = " ".join(context.args).strip()
    if text:
        username = update.effective_user.username or update.effective_user.first_name or "Unknown"
        path = persist_task_markdown("design", username, text)
        await safe_reply(
            update.message,
            f"✅ Дизайн-задача принята и сохранена.\n`{path.name}`",
            parse_mode="Markdown",
        )
        return

    context.user_data["waiting_for_task_kind"] = "design"
    await safe_reply(
        update.message,
        "Пришли описание задачи или фото.\n"
        "Например: фасад, меню, вывеска, интерьер, визуальный концепт.",
    )


async def codex_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_authorized_chat(update):
        return
    set_chat_mode(context, "codex")
    chat_id = str(update.effective_chat.id)
    username = update.effective_user.username or update.effective_user.first_name or "Unknown"
    session_id, _session_path, created = get_or_create_codex_session(chat_id, username)
    created_text = "создана" if created else "продолжена"
    await safe_reply(
        update.message,
        "🤖 `Codex mode` активирован.\n"
        f"Сессия `{session_id}` {created_text}.\n\n"
        "Теперь следующие сообщения не пойдут в RAG, а будут приняты как рабочие задачи.\n"
        "Чтобы вернуться в базу знаний, нажми `📚 База знаний` или используй `/rag`.",
        parse_mode="Markdown",
    )


async def rag_mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    set_chat_mode(context, "rag")
    reset_intake_state(context)
    await safe_reply(
        update.message,
        "📚 Возврат в режим базы знаний.\n"
        "Следующие сообщения снова будут обрабатываться как RAG-запросы.",
    )


async def accept_codex_input(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    kind: str,
    text: str,
    attachments: list[str] | None = None,
) -> None:
    if not await require_authorized_chat(update):
        return
    chat_id = str(update.effective_chat.id)
    username = update.effective_user.username or update.effective_user.first_name or "Unknown"
    session_id, session_path, _created = get_or_create_codex_session(chat_id, username)
    task_id, task_path = materialize_codex_task(
        session_id=session_id,
        kind=kind,
        username=username,
        text=text,
        source_message_id=str(update.message.message_id),
        attachments=attachments,
    )
    update_session_card(
        session_path,
        task_id,
        f"Последняя задача `{task_id}` принята в работу как `{kind}`. "
        "Deep-processing может быть выполнен позже отдельным worker-слоем.",
    )
    await safe_reply(
        update.message,
        "✅ Задача принята в `Codex runtime`.\n"
        f"Session: `{session_id}`\n"
        f"Task: `{task_id}`\n"
        f"Card: `{task_path.name}`",
        parse_mode="Markdown",
    )


# ─── Обработчики ─────────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text in BUTTON_QUERIES:
        await rag_reply(update, BUTTON_QUERIES[text])
        return

    if text == "📊 Статус":
        await status_command(update, context)
        return

    if text == "📝 Заметка":
        context.user_data["waiting_for_note"] = True
        await safe_reply(update.message, "Напишите текст заметки:")
        return

    if text == "🧠 Задача":
        await task_command(update, context)
        return

    if text == "🎨 Дизайн":
        await design_command(update, context)
        return

    if text == "🤖 Codex":
        await codex_command(update, context)
        return

    if text == "📚 База знаний":
        await rag_mode_command(update, context)
        return

    if context.user_data.get("waiting_for_note"):
        context.user_data["waiting_for_note"] = False
        context.user_data["note_text"] = text
        await note_command(update, context)
        return

    waiting_kind = context.user_data.get("waiting_for_task_kind")
    if waiting_kind:
        username = update.effective_user.username or update.effective_user.first_name or "Unknown"
        path = persist_task_markdown(waiting_kind, username, text)
        reset_intake_state(context)
        await safe_reply(
            update.message,
            f"✅ {TASK_KIND_LABELS.get(waiting_kind, waiting_kind).capitalize()} сохранена.\n`{path.name}`",
            parse_mode="Markdown",
        )
        return

    if get_chat_mode(context) == "codex":
        await accept_codex_input(update, context, "codex", text)
        return

    if any(word in text.lower() for word in ["привет", "здравствуй", "hi", "hello"]):
        await safe_reply(
            update.message,
            "Привет! 👋 Задайте вопрос по базе знаний кофейни.",
            reply_markup=MAIN_KEYBOARD,
        )
        return

    await rag_reply(update, text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if get_chat_mode(context) == "codex":
        if not await require_authorized_chat(update):
            return
        chat_id = str(update.effective_chat.id)
        username = update.effective_user.username or update.effective_user.first_name or "Unknown"
        session_id, session_path, _created = get_or_create_codex_session(chat_id, username)
        caption = (update.message.caption or "").strip()
        task_id, task_path = materialize_codex_task(
            session_id=session_id,
            kind="artifact-only" if not caption else "design",
            username=username,
            text=caption,
            source_message_id=str(update.message.message_id),
        )
        artifact_path = await save_codex_photo(update, context, task_id)
        task_content = task_path.read_text(encoding="utf-8")
        task_content = task_content.replace("- нет вложений", f"- `{artifact_path.name}`", 1)
        task_path.write_text(task_content, encoding="utf-8")
        update_session_card(
            session_path,
            task_id,
            f"Последний артефакт `{artifact_path.name}` принят в сессию как задача `{task_id}`.",
        )
        await safe_reply(
            update.message,
            "✅ Материал принят в `Codex runtime`.\n"
            f"Session: `{session_id}`\n"
            f"Task: `{task_id}`\n"
            f"Artifact: `{artifact_path.name}`",
            parse_mode="Markdown",
        )
        return

    waiting_kind = context.user_data.get("waiting_for_task_kind")
    if not waiting_kind:
        await safe_reply(
            update.message,
            "Фото получил. Чтобы превратить его в задачу, нажми `🎨 Дизайн` или используй `/design`.",
            parse_mode="Markdown",
        )
        return

    if not await require_authorized_chat(update):
        return

    username = update.effective_user.username or update.effective_user.first_name or "Unknown"
    caption = (update.message.caption or "").strip()
    photo_path = await save_photo_task(update, context, waiting_kind)
    card_path = persist_task_markdown(
        waiting_kind,
        username,
        caption,
        attachments=[photo_path.name],
    )
    reset_intake_state(context)
    await safe_reply(
        update.message,
        "✅ Входящий материал сохранён.\n"
        f"Карточка: `{card_path.name}`\n"
        f"Файл: `{photo_path.name}`",
        parse_mode="Markdown",
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error: %s", update, context.error)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand("start", "Главное меню"),
        BotCommand("help", "Что умеет бот"),
        BotCommand("status", "Статус RAG API и индекса"),
        BotCommand("note", "Создать заметку"),
        BotCommand("codex", "Перейти в Codex mode"),
        BotCommand("rag", "Вернуться в базу знаний"),
        BotCommand("task", "Принять задачу в inbox"),
        BotCommand("design", "Принять дизайн-задачу или фото"),
    ])


def main() -> None:
    logger.info(
        "🤖 VK-offee AI Bot v3.1 запущен (mode=%s, RAG + Codex menu)",
        BOT_RUNTIME_MODE,
    )

    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("note", note_command))
    application.add_handler(CommandHandler("codex", codex_command))
    application.add_handler(CommandHandler("rag", rag_mode_command))
    application.add_handler(CommandHandler("task", task_command))
    application.add_handler(CommandHandler("design", design_command))
    application.add_handler(CommandHandler("reindex", reindex_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_error_handler(error_handler)

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
        timeout=30,
        bootstrap_retries=-1,
    )


if __name__ == "__main__":
    main()
