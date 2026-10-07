from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_book(self, book_data: SBookAdd) -> BooksModel:
        book = BooksModel(**book_data.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_books(self) -> list[BooksModel]:
        result = await self.session.execute(select(BooksModel).order_by(BooksModel.id))
        return list(result.scalars().all())

    async def get_book(self, book_id: int) -> BooksModel | None:
        return await self.session.get(BooksModel, book_id)

    async def update_book(
        self,
        book: BooksModel,
        book_data: SBookAdd,
    ) -> BooksModel:
        for field, value in book_data.model_dump().items():
            setattr(book, field, value)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: int) -> bool:
        result = await self.session.execute(
            delete(BooksModel).where(BooksModel.id == book_id)
        )
        await self.session.commit()
        return result.rowcount > 0
