import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHAT_ID = int(os.getenv("CHAT_ID"))

# Создаём клиент Telethon
client = TelegramClient("session", API_ID, API_HASH)

# Храним загруженные сообщения
chat_data = {}  # Словарь для хранения данных


async def scrape_chat():
    """Скачивает все старые сообщения из чата и сохраняет их в память"""
    await client.start(PHONE_NUMBER)

    messages = await client.get_messages(CHAT_ID, limit=10)  # Получаем все сообщения
    print(f"📥 Загружено {len(messages)} сообщений.")

    for msg in reversed(messages):
        print()
        print(msg.sender_id)
        print(msg.text)
        print(msg.entities)

    print("✅ История сообщений загружена!")

    return chat_data  # Возвращаем данные
