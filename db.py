from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем данные из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Создаем фабрику сессий
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    async with async_session() as session:
        yield session
