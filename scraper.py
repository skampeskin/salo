import matplotlib.dates as mdates
import os
import asyncio
import json
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import MessageEntityMentionName
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHAT_ID = int(os.getenv("CHAT_ID"))
print(PHONE_NUMBER)

# Создаём клиент Telethon
client = TelegramClient("session", API_ID, API_HASH)

# Храним загруженные сообщения
if os.path.exists(os.getenv("FILE_WITH_HISTORY")):
    with open(os.getenv("FILE_WITH_HISTORY"), "r", encoding="utf-8") as f:
        chat_data = json.load(f) # Словарь для хранения данных
else:
    chat_data = {}

async def process_for_mass(msg: Message):
    chat_data["latest_date"] = max(chat_data.get("latest_date", 0), mdates.date2num(msg.date))
    chat_data["earliest_date"] = min(chat_data.get("earliest_date", 100000), mdates.date2num(msg.date))
    if str(msg.sender_id) != str(os.getenv("EPIC_ID")):
        sender = await msg.get_sender()
        if sender and sender.username is not None:
            if "@" + sender.username not in chat_data:
                chat_data["@" + sender.username] = str(msg.sender_id)
        return
    i = 0
    user_id = None
    diff = None
    res = None
    entities = msg.get_entities_text()
    if len(entities) < 3:
        return
    if isinstance(entities[0][0], MessageEntityMentionName):
        user_id = int(entities[0][0].user_id)
    else:
        return
    if entities[-2][1].isdigit():
        diff = int(entities[-2][1])
    else:
        return
    if entities[-1][1].isdigit():
        res = int(entities[-1][1])
    else:
        return
    if user_id not in chat_data:
        chat_data[user_id] = []
    chat_data[user_id].append([mdates.date2num(msg.date), res])

async def scrape_chat():
    """Скачивает все старые сообщения из чата и сохраняет их в память"""
    num_msgs = 10000
    latest_date = chat_data.get("latest_date", 0)
    async with client:
        i = 0
        async for msg in client.iter_messages(CHAT_ID, limit=num_msgs): # Получаем все сообщения
            if msg.date <= mdates.num2date(latest_date):
                break
            await process_for_mass(msg)
            i += 1
            if i % (num_msgs//10) == 0:
                print(f"{i*100/num_msgs}%")

    print("Скачал")
    with open(os.getenv("FILE_WITH_HISTORY"), "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)
    print(f"✅ История чата сохранена в {os.getenv("FILE_WITH_HISTORY")}")
    return chat_data  # Возвращаем данны
