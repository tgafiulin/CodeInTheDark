import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

# Загрузка токена из .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Создаём машину состояний
class RegistrationState(StatesGroup):
    waiting_for_name = State()  # Ожидаем имя
    waiting_for_surname = State()  # Ожидаем фамилию

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я Telegram-бот, работающий на aiogram 3.x.")

# Обработчик команды /reg
@router.message(Command("reg"))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Привет! Давай начнем регистрацию. Как тебя зовут?")
    # Переходим в состояние ожидания имени
    await state.set_state(RegistrationState.waiting_for_name)

# Обработчик для получения имени
@router.message(StateFilter(RegistrationState.waiting_for_name))  # Используем фильтр состояния
async def get_name(message: Message, state: FSMContext):
    # Сохраняем имя пользователя
    user_name = message.text
    await state.update_data(name=user_name)
    
    await message.answer(f"Отлично, {user_name}! Теперь введи свою фамилию.")
    # Переходим к следующему состоянию для фамилии
    await state.set_state(RegistrationState.waiting_for_surname)

# Обработчик для получения фамилии
@router.message(StateFilter(RegistrationState.waiting_for_surname))  # Используем фильтр состояния
async def get_surname(message: Message, state: FSMContext):
    # Сохраняем фамилию пользователя
    user_surname = message.text
    await state.update_data(surname=user_surname)

    # Получаем полные данные (имя и фамилию)
    user_data = await state.get_data()
    full_name = f"{user_data['name']} {user_data['surname']}"
    
    # Завершаем регистрацию
    await message.answer(f"Регистрация завершена! Ваше имя: {full_name}.")
    
    # Очищаем состояние
    await state.clear()


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
    dp.include_router(router)  # Добавляем маршрутизатор в диспетчер
    await dp.start_polling(bot)  # Передаем объект bot в метод start_polling

if __name__ == "__main__":
    asyncio.run(main())  # Запуск основной асинхронной функции
