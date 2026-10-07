from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from database import Base, engine
from models.books import BooksModel  # noqa: F401
from routers.books import router as books_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Library API",
    description="Асинхронный REST API для управления библиотекой книг.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(books_router)
