#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VK-offee AI Bot v2.0
Telegram бот с доступом к базе знаний GitHub
"""

import os
import logging
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

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
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Путь к репозиторию VK-offee (на уровень выше telegram-bot)
REPO_PATH = Path(__file__).parent.parent.resolve()

# Инициализация OpenAI клиента
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Вспомогательная функция поиска
def search_knowledge_base(query: str, max_results: int = 5):
    """Поиск в базе знаний по запр��су с поддержкой таблиц"""
    knowledge_base = REPO_PATH / "knowledge-base"
    results = []

    if not knowledge_base.exists():
        logger.warning(f"Knowledge base not found at: {knowledge_base}")
        return []

    logger.info(f"Searching for: '{query}' in {knowledge_base}")
    files_checked = 0

    for file_path in knowledge_base.rglob("*"):
        if not file_path.is_file():
            continue

        files_checked += 1

        # Исключаем служебные и неактуальные файлы
        path_str = str(file_path).lower()
        exclude_patterns = ['sync-report', 'отчет синхронизации', 'неактуально', 'неактуальн']
        if any(pattern in path_str for pattern in exclude_patterns):
            continue

        # Обработка таблиц (CSV, Excel)
        if file_path.suffix in ['.csv', '.xlsx', '.xls']:
            try:
                # Читаем таблицу
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
                else:
                    df = pd.read_excel(file_path)

                # Ищем во всех ячейках таблицы
                found = False
                for col in df.columns:
                    for idx, value in df[col].items():
                        if pd.notna(value) and query.lower() in str(value).lower():
                            # Формируем контекст: показываем всю строку с найденным значением
                            row_data = df.iloc[idx].to_dict()
                            context_parts = [f"{k}: {v}" for k, v in row_data.items() if pd.notna(v)]
                            context = " | ".join(context_parts)  # Все колонки

                            results.append({
                                'file': str(file_path.relative_to(REPO_PATH)),
                                'context': context[:500]  # Увеличил лимит до 500 символов
                            })
                            found = True
                            break
                    if found:
                        break
            except Exception:
                # Если не удалось прочитать таблицу, пробуем как текст
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if query.lower() in content.lower():
                        lines = content.split('\n')
                        for line in lines:
                            if query.lower() in line.lower():
                                results.append({
                                    'file': str(file_path.relative_to(REPO_PATH)),
                                    'context': line.strip()[:200]
                                })
                                break
                except Exception:
                    pass

        # Обработка текстовых файлов (MD, TXT)
        elif file_path.suffix in ['.md', '.txt']:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower():
                    lines = content.split('\n')
                    for line in lines:
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

    logger.info(f"Search completed. Files checked: {files_checked}, Results found: {len(results)}")
    return results

def generate_ai_response(user_question: str, search_results: list) -> str:
    """Генерация умного ответа с помощью ChatGPT на основе найденной информации"""

    logger.info(f"Generating AI response for question: '{user_question}' with {len(search_results)} search results")

    if not openai_client:
        return "⚠️ AI-функции недоступны. Проверьте настройки API ключа."

    # Формируем контекст из результатов поиска
    context_parts = []
    for result in search_results[:5]:  # Берем первые 5 результатов
        context_parts.append(f"Файл: {result['file']}\nИнформация: {result['context']}")

    context = "\n\n".join(context_parts) if context_parts else "Информация не найдена в базе знаний."

    # Логируем контекст для отладки
    logger.info(f"Context being sent to ChatGPT:\n{context[:1000]}")

    # Формируем промпт для ChatGPT
    system_prompt = """Ты - AI-ассистент сети кофеен «Вкусный Кофе».
Твоя задача - отвечать на вопросы сотрудников и менеджеров на основе информации из базы знаний.

Правила:
- Отвечай кратко и по делу
- Используй только информацию из предоставленного контекста
- Если информации нет в контексте, честно скажи об этом
- Форматируй ответ понятно (используй списки, если нужно)
- Говори на русском языке
- Будь дружелюбным и профессиональным"""

    user_prompt = f"""Вопрос пользователя: {user_question}

Информация из базы знаний:
{context}

Ответь на вопрос пользователя на основе этой информации."""

    try:
        # Вызываем OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return f"❌ Ошибка при генерации ответа: {str(e)}"

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    # Создаём кнопки меню
    keyboard = [
        [KeyboardButton("🔍 Поиск"), KeyboardButton("📋 Меню")],
        [KeyboardButton("👥 Роли"), KeyboardButton("📊 Статус")],
        [KeyboardButton("❓ Помощь")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🤖 VK-offee AI Bot v2.0\n\n"
        "Я помогу вам работать с базой знаний сети кофеен «Вкусный Кофе».\n\n"
        "Используйте кнопки ниже или просто напишите вопрос! 👇",
        reply_markup=reply_markup
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

    # Обработка кнопок меню
    if text == "🔍 Поиск":
        await update.message.reply_text(
            "Введите запрос для поиска в базе знаний.\n\n"
            "Например:\n"
            "• кофе\n"
            "• боул с индейкой\n"
            "• калькуляция"
        )
        return
    elif text == "📋 Меню":
        await menu_command(update, context)
        return
    elif text == "👥 Роли":
        await roles_command(update, context)
        return
    elif text == "📊 Статус":
        await status(update, context)
        return
    elif text == "❓ Помощь":
        await help_command(update, context)
        return

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

    # Стоп-слова для фильтрации
    stop_words = {'какая', 'какой', 'какие', 'где', 'как', 'что', 'это', 'есть',
                  'был', 'была', 'были', 'будет', 'для', 'или', 'при', 'так',
                  'вот', 'мой', 'твой', 'его', 'её', 'чем', 'том', 'тот'}

    # Убираем знаки препинания и извлекаем ключевые слова
    import re
    text_clean = re.sub(r'[^\w\s]', ' ', text_lower)  # Убираем знаки препинания
    keywords = [word for word in text_clean.split() if len(word) > 3 and word not in stop_words]

    # Добавляем синонимы для популярных запросов
    synonyms = {
        'зарплата': ['з/п', 'оплата', 'зарплат'],
        'зарплат': ['з/п', 'оплата'],
        'себестоимость': ['себестоим', 'стоимость'],
        'рецепт': ['приготовление', 'готовить'],
        'повар': ['повар', 'кухня'],
        'официант': ['официант', 'раннер'],
    }

    # Расширяем список ключевых с��ов синонимами
    expanded_keywords = []
    for keyword in keywords:
        expanded_keywords.append(keyword)
        # Проверяем, есть ли синонимы для этого слова
        for main_word, syns in synonyms.items():
            if keyword in main_word or main_word in keyword:
                expanded_keywords.extend(syns)
                break

    # Поиск по каждому ключевому слову
    all_results = []
    for keyword in expanded_keywords[:6]:  # Ограничиваем первыми 6 ключевыми словами
        results = search_knowledge_base(keyword, max_results=3)
        all_results.extend(results)

    # Убираем дубликаты
    unique_results = list({r['file']: r for r in all_results}.values())

    # Генерируем умный ответ с помощью GPT
    ai_response = generate_ai_response(text, unique_results)

    await update.message.reply_text(ai_response)

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
