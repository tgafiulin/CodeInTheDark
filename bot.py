# bot.py
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import os
import logging
import asyncio
from dotenv import load_dotenv
from registration import router as registration_router  # Импортируем маршрутизатор из registration.py


# Загрузка токена из .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Основной маршрутизатор
main_router = Router()

# Подключаем роутеры
dp.include_router(registration_router)
dp.include_router(main_router)  # Основной роутер  # Роутер для регистрации

# Обработчик команды /start
@main_router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я Telegram-бот, работающий на aiogram 3.x.")

# Обработчик команды /help
@main_router.message(Command("help"))
async def send_help(message: Message):
    await message.answer("Я могу делать много чего! Пока просто скажи 'Привет'.")

# Обработчик текстовых сообщений
@main_router.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# Основная функция
async def main():
    await dp.start_polling(bot)  # Запуск бота

if __name__ == "__main__":
    asyncio.run(main())  # Запуск основной асинхронной функции
