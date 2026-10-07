from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from database import create_tables
from routers.books import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await create_tables()
    yield


app = FastAPI(
    title="My Library API",
    description="Асинхронный REST API для управления книгами.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(books_router)


@app.get("/", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "my-library"}
