import logging
import random

logger = logging.getLogger(__name__)

# В качестве БД используем словарь
# Хранит информацию о загаданных числах
GUSS_NUMBER_DB: dict[int, int] = {}


def create_guess_number(chat_id: int) -> int:
    """Генерируем рандомное число"""

    number = random.randint(1, 100)
    logger.info(f"Сгенерировано число: {number}")

    GUSS_NUMBER_DB[chat_id] = number
    logger.info(f"chat_id: {chat_id}")
    return number


def get_guess_number(chat_id: int) -> int:
    """Возвращаем сгенерированное число.

    Если число отсутсвует в БД - создаем новый."""

    guess_number = GUSS_NUMBER_DB.get(chat_id, None)
    if guess_number is None:
        return create_guess_number(chat_id)

    return guess_number
