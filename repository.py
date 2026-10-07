from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BookModel
from schemas.books import SBookAdd


class BookRepository:
    """Единственный слой приложения, который напрямую работает с SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_book(self, book_data: SBookAdd) -> BookModel:
        book = BookModel(**book_data.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_books(self) -> list[BookModel]:
        result = await self.session.execute(select(BookModel).order_by(BookModel.id))
        return list(result.scalars().all())

    async def get_book_by_id(self, book_id: int) -> BookModel | None:
        return await self.session.get(BookModel, book_id)

    async def update_book(self, book_id: int, book_data: SBookAdd) -> BookModel | None:
        book = await self.get_book_by_id(book_id)
        if book is None:
            return None

        for field, value in book_data.model_dump().items():
            setattr(book, field, value)

        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: int) -> bool:
        book = await self.get_book_by_id(book_id)
        if book is None:
            return False

        await self.session.execute(delete(BookModel).where(BookModel.id == book_id))
        await self.session.commit()
        return True
