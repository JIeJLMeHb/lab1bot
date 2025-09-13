from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
import pandas as pd
import asyncio
import os

import spaceflightnews as sfn
import finance as fin
import weather as wt
import logger as lg
from key import TOKEN


global USERNAME

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
@lg.logging
async def start(msg: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="☁️Данные о погоде☀️")],
            [types.KeyboardButton(text="🚀Информация о событиях в сфере космических полётов")],
            [types.KeyboardButton(text="💲Курс доллара💵")],
        ],
        resize_keyboard=True
    )
    USERNAME = msg.from_user.first_name
    return await msg.reply(
        f"Здраствуйте, {USERNAME}! Выберите действие из кнопочек снизу:",
        reply_markup=keyboard
    )

@dp.message()
@lg.logging
async def handle_buttons(msg: Message):
    text = msg.text
    if text == "☁️Данные о погоде☀️":
        return await msg.answer(wt.get_weather())
    elif text == "🚀Информация о событиях в сфере космических полётов":
        return await msg.answer(sfn.get_spaceflight_summary())
    elif text == "💲Курс доллара💵":
        return await msg.answer(fin.get_curse())
    else:
        return await msg.answer(f'Вы написали "{text}", я не знаю такой команды...')

async def main():
    print("Начат запуск основных систем бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
