from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from repository import BookRepository
from schemas.books import SBook, SBookAdd

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def add_book(
    book_data: SBookAdd,
    session: AsyncSession = Depends(get_session),
) -> SBook:
    return await BookRepository(session).add_book(book_data)


@router.get("", response_model=list[SBook], status_code=status.HTTP_200_OK)
async def get_books(
    session: AsyncSession = Depends(get_session),
) -> list[SBook]:
    return await BookRepository(session).get_books()


@router.get("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_session),
) -> SBook:
    book = await BookRepository(session).get_book_by_id(book_id)
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
    session: AsyncSession = Depends(get_session),
) -> SBook:
    book = await BookRepository(session).update_book(book_id, book_data)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await BookRepository(session).delete_book(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
