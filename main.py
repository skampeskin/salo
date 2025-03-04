import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from scraper import scrape_chat # Импортируем scraper
from handlers import first_handler
import datetime

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ин

# Храним загруженные сообщения в памяти
chat_history = {}


async def main():
    global chat_history
    print("📥 Загружаем историю сообщений...")
    dp = Dispatcher()  # потом поменять, тк это оперативная память
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN)
    dp.include_routers(first_handler.router)
    #await bot.send_message(os.getenv("CHAT_ID"), f"Качаю дату")
    #cur_time = datetime.datetime.now()
    chat_history = await scrape_chat()  # Загружаем старые сообщения
    #await bot.send_message(os.getenv("CHAT_ID"), f"Скачал все сообщения до {cur_time}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
