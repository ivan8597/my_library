from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from repository import BookRepository
from schemas.books import SBook, SBookAdd

router = APIRouter(prefix="/books", tags=["Книги"])


def get_repository(session: AsyncSession = Depends(get_session)) -> BookRepository:
    return BookRepository(session)


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def add_book(
    book_data: SBookAdd,
    repository: BookRepository = Depends(get_repository),
) -> SBook:
    return await repository.add_book(book_data)


@router.get("", response_model=list[SBook], status_code=status.HTTP_200_OK)
async def get_books(
    repository: BookRepository = Depends(get_repository),
) -> list[SBook]:
    return await repository.get_books()


@router.get("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def get_book(
    book_id: int,
    repository: BookRepository = Depends(get_repository),
) -> SBook:
    book = await repository.get_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
    return book


@router.put("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def update_book(
    book_id: int,
    book_data: SBookAdd,
    repository: BookRepository = Depends(get_repository),
) -> SBook:
    book = await repository.get_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
    return await repository.update_book(book, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    repository: BookRepository = Depends(get_repository),
) -> None:
    deleted = await repository.delete_book(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
