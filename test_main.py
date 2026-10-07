from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

import database
from main import app


@pytest_asyncio.fixture
async def test_client(tmp_path: Path):
    database_path = tmp_path / "test_library.db"
    test_engine = database.create_async_engine(
        f"sqlite+aiosqlite:///{database_path}",
        echo=False,
    )
    test_session = database.async_sessionmaker(
        bind=test_engine,
        class_=database.AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_session():
        async with test_session() as session:
            yield session

    from models.books import BookModel  # noqa: F401

    async with test_engine.begin() as connection:
        await connection.run_sync(database.Base.metadata.create_all)

    app.dependency_overrides[database.get_session] = override_get_session
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_book_crud(test_client: AsyncClient):
    response = await test_client.post(
        "/books",
        json={
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "pages": 328,
        },
    )
    assert response.status_code == 201
    book = response.json()
    assert book["is_read"] is False

    book_id = book["id"]
    response = await test_client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await test_client.put(
        f"/books/{book_id}",
        json={
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "pages": 328,
            "is_read": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["is_read"] is True

    response = await test_client.delete(f"/books/{book_id}")
    assert response.status_code == 204
    assert response.text == ""

    response = await test_client.get(f"/books/{book_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Книга не найдена"


@pytest.mark.asyncio
async def test_pages_validation(test_client: AsyncClient):
    response = await test_client.post(
        "/books",
        json={"title": "Short", "author": "Author", "year": 2026, "pages": 10},
    )
    assert response.status_code == 422
