from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio

import spaceflightnews as sfn
import finance as fin
import weather as wt
import logger as lg

from key import TOKEN


global USERNAME

class WeatherState(StatesGroup):
    waiting_for_city = State()

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

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

@dp.message(WeatherState.waiting_for_city)
@lg.logging
async def process_city(msg: Message, state: FSMContext):
    city = msg.text
    weather_info = wt.get_weather(city)
    await msg.answer(weather_info)
    await state.clear()

@dp.message()
@lg.logging
async def handle_buttons(msg: Message, state: FSMContext):
    text = msg.text
    if text == "☁️Данные о погоде☀️":
        await msg.answer("Введите название города:")
        await state.set_state(WeatherState.waiting_for_city)
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
