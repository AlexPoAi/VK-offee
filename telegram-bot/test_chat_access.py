#!/usr/bin/env python3
"""
Тестовый скрипт для проверки доступа к чату кофейни
"""
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

async def test_chat_access():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

    # Получаем информацию о боте
    me = await bot.get_me()
    print(f"✅ Бот: @{me.username}")
    print(f"   ID: {me.id}")

    # Получаем список обновлений (последние сообщения)
    updates = await bot.get_updates(limit=10)

    print(f"\n📨 Последние {len(updates)} обновлений:")
    for update in updates:
        if update.message:
            chat = update.message.chat
            print(f"\n  Chat ID: {chat.id}")
            print(f"  Title: {chat.title if chat.title else 'Private'}")
            print(f"  Type: {chat.type}")
            print(f"  Message: {update.message.text[:50] if update.message.text else 'No text'}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(test_chat_access())
