from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.future import select  # Импорт функции select

# Создаём машину состояний
class RegistrationState(StatesGroup):
    waiting_for_name = State()  # Ожидаем имя
    waiting_for_surname = State()  # Ожидаем фамилию

router = Router()

# Обработчик команды /reg
@router.message(Command("reg"))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Привет! Давай начнем регистрацию в Code in the Dark.")
    await message.answer("Введи своё имя:")
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

@router.message(StateFilter(RegistrationState.waiting_for_surname))
async def get_surname(message: Message, state: FSMContext):
    from db import get_db_session  # Убедитесь, что импорт корректный
    from models import User  # Импорт модели пользователя

    # Получаем фамилию пользователя
    user_surname = message.text
    await state.update_data(surname=user_surname)

    # Получаем данные из состояния
    user_data = await state.get_data()
    first_name = user_data['name']
    last_name = user_surname

    # Получаем chat_id и nickname
    chat_id = message.from_user.id
    nickname = message.from_user.username

    # Работа с базой данных
    async for session in get_db_session():
        # Проверяем, есть ли пользователь уже в базе
        result = await session.execute(select(User).where(User.chat_id == chat_id))
        existing_user = result.scalars().first()

        if existing_user:
            # Если пользователь существует, обновляем его данные
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.nickname = nickname
        else:
            # Если пользователь не найден, создаем новую запись
            new_user = User(
                chat_id=chat_id,
                nickname=nickname,
                first_name=first_name,
                last_name=last_name
            )
            session.add(new_user)

        # Сохраняем изменения в базе
        await session.commit()

    # Завершаем регистрацию
    await message.answer(f"Регистрация завершена! Ваши данные:\nИмя: {first_name}\nФамилия: {last_name}.")
    await state.clear()
