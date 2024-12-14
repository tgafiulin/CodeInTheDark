import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
import os
from dotenv import load_dotenv

# Загрузка токена из .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я Telegram-бот, работающий на aiogram 3.x.")

# Обработчик команды /help
@router.message(Command("help"))
async def send_help(message: Message):
    await message.answer("Я могу делать много чего! Пока просто скажи 'Привет'.")

# Обработчик текстовых сообщений
@router.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
