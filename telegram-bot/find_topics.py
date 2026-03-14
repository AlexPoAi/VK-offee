#!/usr/bin/env python3
"""
Поиск топиков (подчатов) в группе
"""
import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = -1002402720559  # Кофейня ВКУСНЫЙ КОФЕ
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def find_topics():
    bot = Bot(token=BOT_TOKEN)

    print(f"🔍 Проверяю обновления...")

    updates = await bot.get_updates(limit=100)

    print(f"\n📨 Найдено обновлений: {len(updates)}\n")

    for update in updates:
        if update.message:
            msg = update.message
            chat = msg.chat

            if chat.id == CHAT_ID:
                thread_id = msg.message_thread_id if hasattr(msg, 'message_thread_id') else None

                print(f"Chat: {chat.title}")
                print(f"  Message ID: {msg.message_id}")
                print(f"  Thread ID: {thread_id}")
                print(f"  Text: {msg.text[:50] if msg.text else 'No text'}")
                print(f"  Has photo: {bool(msg.photo)}")
                print()

if __name__ == '__main__':
    asyncio.run(find_topics())
