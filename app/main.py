import logging
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web
from const import (GUESS_NUMBER_IS_GREATER_MESSAGE,
                   GUESS_NUMBER_IS_LESS_MESSAGE, USER_GUESSED_MESSAGE,
                   WELCOME_MESSAGE)

from db import create_guess_number, get_guess_number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Переменные окружения
BOT_TOKEN = getenv("BOT_TOKEN")     # необходимо указать в переменных окружения
PORT = int(getenv("PORT"))  # не указываем, берется автоматически

# Бот
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(msg: types.Message) -> None:
    """Обработчик команды /start"""

    create_guess_number(chat_id=msg.chat.id)
    await msg.answer(text=WELCOME_MESSAGE)


@dp.message()
async def message_handler(msg: types.Message) -> None:
    """Обработчик сообщений"""
    try:
        number = int(msg.text)
        logger.info(f"Пользователь ввел число: {number}")

        guess_number = get_guess_number(chat_id=msg.chat.id)
        if number > guess_number:
            await msg.answer(GUESS_NUMBER_IS_LESS_MESSAGE)
        elif number < guess_number:
            await msg.answer(GUESS_NUMBER_IS_GREATER_MESSAGE)
        else:
            await msg.answer(USER_GUESSED_MESSAGE)
    except (TypeError, ValueError):
        await msg.answer("Введите целое число!")


# API
routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    """Используется для health check"""
    return web.Response(text="OK")


@routes.post(f"/{BOT_TOKEN}")
async def handle_webhook_request(request):
    """Обрабатывает webhook из telegram"""

    # Достаем токен
    url = str(request.url)
    index = url.rfind("/")
    token = url[index + 1 :]

    # Проверяем токен
    if token == BOT_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp._process_update(bot=bot, update=update)

        return web.Response(text="OK")
    else:
        return web.Response(status=403)


if __name__ == "__main__":
    logger.info("Сервер заработал ...")

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=PORT)
