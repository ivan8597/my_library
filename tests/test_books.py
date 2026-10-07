import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from database import Base, engine, AsyncSessionLocal
from main import app
from models.books import BooksModel


@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with AsyncSessionLocal() as session:
        await session.execute(delete(BooksModel))
        await session.commit()


@pytest.mark.asyncio
async def test_books_crud() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        created = await client.post(
            "/books",
            json={
                "title": "Мастер и Маргарита",
                "author": "Михаил Булгаков",
                "year": 1967,
                "pages": 480,
            },
        )
        assert created.status_code == 201
        book_id = created.json()["id"]

        listed = await client.get("/books")
        assert listed.status_code == 200
        assert len(listed.json()) == 1

        received = await client.get(f"/books/{book_id}")
        assert received.status_code == 200
        assert received.json()["is_read"] is False

        updated = await client.put(
            f"/books/{book_id}",
            json={
                "title": "Мастер и Маргарита",
                "author": "М. А. Булгаков",
                "year": 1967,
                "pages": 480,
                "is_read": True,
            },
        )
        assert updated.status_code == 200
        assert updated.json()["is_read"] is True

        deleted = await client.delete(f"/books/{book_id}")
        assert deleted.status_code == 204

        missing = await client.get(f"/books/{book_id}")
        assert missing.status_code == 404
        assert missing.json()["detail"] == "Книга не найдена"


@pytest.mark.asyncio
async def test_pages_must_be_greater_than_ten() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/books",
            json={
                "title": "Короткая книга",
                "author": "Автор",
                "year": 2026,
                "pages": 10,
            },
        )
    assert response.status_code == 422
