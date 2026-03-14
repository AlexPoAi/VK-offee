#!/usr/bin/env python3
"""
Скрипт для скачивания накладных из чата кофейни
"""
import os
import asyncio
from pathlib import Path
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = -1002402720559  # Кофейня ВКУСНЫЙ КОФЕ
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OUTPUT_DIR = Path(__file__).parent.parent / "invoices" / "raw"

async def fetch_photos_from_chat(limit=100):
    """Скачать фото из чата"""
    bot = Bot(token=BOT_TOKEN)

    # Создаём папку для фото
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Получаю последние {limit} сообщений из чата...")

    # Получаем историю сообщений
    messages = []
    offset = 0

    # Telegram API не даёт прямого доступа к истории через get_updates
    # Нужно использовать метод get_chat_history или читать через updates

    print(f"⚠️ Для доступа к истории чата нужно:")
    print(f"   1. Бот должен быть администратором")
    print(f"   2. Использовать MTProto API (не Bot API)")
    print(f"\n💡 Альтернатива: Перешли мне несколько накладных в личку боту")
    print(f"   Тогда я смогу их обработать через get_updates()")

    # Проверяем последние updates
    updates = await bot.get_updates(limit=100)

    photo_count = 0
    for update in updates:
        if update.message and update.message.photo:
            chat = update.message.chat
            if chat.id == CHAT_ID:
                # Скачиваем фото
                photo = update.message.photo[-1]  # Берём самое большое
                file = await bot.get_file(photo.file_id)

                timestamp = update.message.date.strftime("%Y%m%d_%H%M%S")
                filename = f"invoice_{timestamp}_{photo.file_id}.jpg"
                filepath = OUTPUT_DIR / filename

                await file.download_to_drive(filepath)
                print(f"✅ Скачано: {filename}")
                photo_count += 1

    print(f"\n📊 Итого скачано фото: {photo_count}")
    print(f"📁 Папка: {OUTPUT_DIR}")

    return photo_count

if __name__ == '__main__':
    asyncio.run(fetch_photos_from_chat())
