from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Глобальная переменная для истории сообщений (получаем из main.py)
chat_history = {}


def set_chat_data(data):
    """Функция для передачи истории сообщений из main.py"""
    global chat_history
    chat_history = data


@dp.message(commands=["find"])
async def find_message(message: Message):
    """Ищет сообщение по ключевому слову"""
    query = message.text.split(maxsplit=1)[-1]  # Получаем текст запроса

    if not query or query.startswith("/find"):
        await message.answer("⚠ Использование: /find [текст]")
        return

    results = [msg for msg in chat_history.get("messages", []) if query.lower() in msg["text"].lower()]

    if results:
        response = "\n".join([f"{msg['date']} - {msg['text']}" for msg in results[:5]])  # Первые 5 результатов
        await message.answer(f"🔎 Найдено:\n{response}")
    else:
        await message.answer("❌ Ничего не найдено.")
