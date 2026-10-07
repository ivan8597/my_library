from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./library.db"


class Base(DeclarativeBase):
    """Базовый класс для всех SQLAlchemy-моделей."""


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Выдаёт роутеру сессию БД и закрывает её после запроса."""
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    """Создаёт таблицы, если они ещё не существуют."""
    from models.books import BookModel  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
