import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from scraper import scrape_chat # Импортируем scraper
import datetime

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Храним загруженные сообщения в памяти
chat_history = {}


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Бот запущен! 🔥")


@dp.message(Command("history"))
async def show_history(message: Message):
    """Отправляет список последних 5 сообщений из истории"""
    last_messages = chat_history.get("messages", [])[-5:]  # Берём последние 5 сообщений

    if not last_messages:
        await message.answer("История чата пока пуста.")
        return

    history_text = "\n".join([f"{msg['date']} - {msg['text']}" for msg in last_messages])
    await message.answer(f"🕰 История чата:\n{history_text}")


async def main():
    global chat_history
    print("📥 Загружаем историю сообщений...")
    await bot.send_message(os.getenv("CHAT_ID"), f"Качаю дату")
    cur_time = datetime.datetime.now()
    chat_history = await scrape_chat()  # Загружаем старые сообщения
    await bot.send_message(os.getenv("CHAT_ID"), f"Скачал все сообщения до {cur_time}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
