#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VK-offee AI Bot v2.0
Telegram бот с доступом к базе знаний GitHub
"""

import os
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7978142264:AAFr3oSP_ZNz18X_Z9ADCNAs3_lhwIZrfmU')
REPO_PATH = Path(__file__).parent.parent  # Путь к репозиторию VK-offee

# Вспомогательная функция поиска
def search_knowledge_base(query: str, max_results: int = 5):
    """Поиск в базе знаний по запросу"""
    knowledge_base = REPO_PATH / "knowledge-base"
    results = []

    if not knowledge_base.exists():
        return []

    for file_path in knowledge_base.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.md', '.csv', '.txt']:
            # Поиск в названии файла
            if query.lower() in file_path.name.lower():
                results.append({
                    'file': str(file_path.relative_to(REPO_PATH)),
                    'context': f"Найдено в названии файла"
                })
                continue

            # Поиск в содержимом файла
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower():
                    # Найти контекст вокруг запроса
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if query.lower() in line.lower():
                            results.append({
                                'file': str(file_path.relative_to(REPO_PATH)),
                                'context': line.strip()[:200]
                            })
                            break
            except Exception:
                pass

            if len(results) >= max_results:
                break

    return results

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "🤖 VK-offee AI Bot v2.0\n\n"
        "Я помогу вам работать с базой знаний сети кофеен «Вкусный Кофе».\n\n"
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/search <запрос> - Поиск в базе знаний\n"
        "/status - Статус бота\n"
        "/menu - Показать меню кофейни\n"
        "/roles - Список ролей (F1-F9)"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        "📚 Помощь по боту\n\n"
        "Я могу:\n"
        "• Искать информацию в базе знаний\n"
        "• Показывать документы по ролям (F1-F9)\n"
        "• Отвечать на вопросы о процессах\n"
        "• Показывать меню и рецепты\n\n"
        "Просто напишите мне вопрос или используйте команды!"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status"""
    # Проверка доступа к репозиторию
    repo_exists = REPO_PATH.exists()
    content_dir = REPO_PATH / "content"
    content_exists = content_dir.exists()

    status_text = (
        f"🟢 Бот работает!\n\n"
        f"📁 Репозиторий: {'✅' if repo_exists else '❌'}\n"
        f"📂 База знаний: {'✅' if content_exists else '❌'}\n"
        f"📍 Путь: {REPO_PATH}\n"
    )

    await update.message.reply_text(status_text)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /search"""
    query = ' '.join(context.args) if context.args else None

    if not query:
        await update.message.reply_text(
            "Использование: /search <запрос>\n"
            "Например: /search бариста"
        )
        return

    await update.message.reply_text(f"🔍 Ищу информацию по запросу: {query}...")

    results = search_knowledge_base(query)

    if results:
        response = f"✅ Найдено результатов: {len(results)}\n\n"
        for r in results:
            response += f"📄 {r['file']}\n💬 {r['context']}\n\n"
    else:
        response = f"❌ По запросу '{query}' ничего не найдено.\nПопробуйте другие ключевые слова."

    await update.message.reply_text(response)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu"""
    menu_file = REPO_PATH / "content" / "2.VkusnyCoffeeNetwork" / "2.2.Architecture" / "menu"

    if menu_file.exists():
        await update.message.reply_text(
            "📋 Меню кофейни\n\n"
            "Раздел меню находится в разработке.\n"
            f"Путь: {menu_file}"
        )
    else:
        await update.message.reply_text(
            "⚠️ Меню не найдено в базе знаний"
        )

async def roles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /roles - показать роли FPF"""
    roles_text = (
        "🎯 Роли FPF (таблица 3×3)\n\n"
        "**Надсистема (Suprasystem):**\n"
        "F1 - Предприниматель-Контекст\n"
        "F2 - Инженер-Окружение\n"
        "F3 - Менеджер-Взаимодействие\n\n"
        "**Целевая система (System-of-Interest):**\n"
        "F4 - Предприниматель-Требования\n"
        "F5 - Инженер-Архитектура\n"
        "F6 - Менеджер-Реализация\n\n"
        "**Система создания (Constructor):**\n"
        "F7 - Предприниматель-Принципы\n"
        "F8 - Инженер-Платформа\n"
        "F9 - Менеджер-Команда"
    )
    await update.message.reply_text(roles_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    text = update.message.text
    text_lower = text.lower()

    # Обработка приветствий
    if any(word in text_lower for word in ['привет', 'здравствуй', 'hi', 'hello']):
        await update.message.reply_text(
            "Привет! 👋\n"
            "Я бот базы знаний VK-offee.\n"
            "Задавайте любые вопросы!"
        )
        return

    # Для всех остальных сообщений - поиск в базе знаний
    await update.message.reply_text("🔍 Ищу информацию...")

    # Извлекаем ключевые слова (слова длиннее 3 символов)
    keywords = [word for word in text_lower.split() if len(word) > 3]

    # Поиск по каждому ключевому слову
    all_results = []
    for keyword in keywords[:3]:  # Ограничиваем первыми 3 ключевыми словами
        results = search_knowledge_base(keyword, max_results=3)
        all_results.extend(results)

    # Убираем дубликаты
    unique_results = {r['file']: r for r in all_results}.values()

    if unique_results:
        response = "✅ Нашёл информацию:\n\n"
        for r in list(unique_results)[:5]:
            response += f"📄 {r['file']}\n💬 {r['context']}\n\n"
    else:
        response = "❌ К сожалению, не нашёл информацию по вашему вопросу.\nПопробуйте переформулировать или используйте /help"

    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Запуск бота"""
    logger.info("🤖 VK-offee AI Bot v2.0 запущен с доступом к GitHub!")

    # Создание приложения
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("roles", roles_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
