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
    print("⏸️ Обработка фото из рабочего чата временно отключена")
    return 0

if __name__ == '__main__':
    asyncio.run(fetch_photos_from_chat())
