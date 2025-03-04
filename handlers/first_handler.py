import io
import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandObject, Command
from aiogram.types import Message, InputFile, BufferedInputFile
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from dotenv import load_dotenv
import numpy as np

# Загружаем переменные окружения
load_dotenv()

router = Router()


@router.message(Command("plot"))
async def plot_masses(message: Message, command: CommandObject):
    with open(os.getenv("FILE_WITH_HISTORY"), "r", encoding="utf-8") as f:
        chat_history = json.load(f)
    print(chat_history)
    query = command.args
    if not query:
        await message.reply("анлак")
        return

    users = list(command.args.split())  # Преобразуем аргументы в float

    if len(users) < 1:
        await message.reply("анлак3")
        return
    for user in users:
        if user not in chat_history or chat_history[user] not in chat_history:
            await message.reply("Кто-то из этих людей давненько не растил хряка")
            return
    text = f"данные с {mdates.num2date(chat_history["earliest_date"])}\nпо {mdates.num2date(chat_history["latest_date"])}\n"
    for user in users:
        text += user + ": "
        user_id = chat_history[user]
        xy = np.array(sorted(chat_history[user_id]))
        text += f"растил {len(xy) - 1} раз, "
        if len(xy) != 1:
            text += f"avg growth {round(float((xy[-1, 1] - xy[0, 1])/(len(xy)-1)), 5)}\n"
        plt.plot(mdates.num2date(xy[::, 0]), xy[::, 1], label=user)
    plt.xlabel("time")
    plt.ylabel("weight kg")
    plt.title("please fucking work")
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.grid()

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format="png")  # Сохраняем в поток
    plt.close()  # Закрываем график
    image_stream.seek(0)  # Перемещаемся в начало

    # 🔹 5. Отправляем изображение в Telegram
    photo = BufferedInputFile(image_stream.read(), filename="chart.png")
    await message.reply_photo(photo=photo, caption=text)

