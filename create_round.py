from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_start = KeyboardButton(text='Начать раунд')
greet_kb = ReplyKeyboardMarkup(keyboard=[[button_start]],resize_keyboard=True)

create_round_router = Router()

# Обработчик команды /buttons
@create_round_router.message(Command("buttons"))
async def send_help(message: Message):
    await message.reply("Привет!", reply_markup=greet_kb)

# Обработчик для кнопки "Начать раунд" с фильтром
@create_round_router.message(lambda message: message.text == "Начать раунд")
async def handle_start_round(message: Message):
    await message.answer("Раунд начат!", reply_markup=ReplyKeyboardRemove())

