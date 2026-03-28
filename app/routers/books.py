from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import author as crud_author
from app.crud import book as crud_book
from app.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


def _get_or_404(book_id: int, db: Session) -> crud_book.Book:
    book = crud_book.get(db, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("/", response_model=list[BookResponse], summary="書籍一覧取得")
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[crud_book.Book]:
    return crud_book.get_list(db, skip=skip, limit=limit, author_id=author_id)


@router.post(
    "/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="書籍登録"
)
def create_book(data: BookCreate, db: Session = Depends(get_db)) -> crud_book.Book:
    if crud_author.get(db, data.author_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author id={data.author_id} not found",
        )
    return crud_book.create(db, data)


@router.get("/{book_id}", response_model=BookResponse, summary="書籍取得")
def get_book(book_id: int, db: Session = Depends(get_db)) -> crud_book.Book:
    return _get_or_404(book_id, db)


@router.put("/{book_id}", response_model=BookResponse, summary="書籍更新")
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)) -> crud_book.Book:
    book = _get_or_404(book_id, db)
    if data.author_id is not None and crud_author.get(db, data.author_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author id={data.author_id} not found",
        )
    return crud_book.update(db, book, data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="書籍削除")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    book = _get_or_404(book_id, db)
    crud_book.delete(db, book)
