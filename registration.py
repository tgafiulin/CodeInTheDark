from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Создаём машину состояний
class RegistrationState(StatesGroup):
    waiting_for_name = State()  # Ожидаем имя
    waiting_for_surname = State()  # Ожидаем фамилию

router = Router()

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
