from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.use_cases.book import BookUseCase
from app.domain.exceptions import NotFoundError
from app.infrastructure.database import get_db
from app.infrastructure.repositories.author import SqlAlchemyAuthorRepository
from app.infrastructure.repositories.book import SqlAlchemyBookRepository
from app.presentation.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


def get_book_use_case(db: Session = Depends(get_db)) -> BookUseCase:
    return BookUseCase(
        repo=SqlAlchemyBookRepository(db),
        author_repo=SqlAlchemyAuthorRepository(db),
    )


@router.get("/", response_model=list[BookResponse], summary="書籍一覧取得")
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    use_case: BookUseCase = Depends(get_book_use_case),
) -> list[BookResponse]:
    books = use_case.list_books(skip=skip, limit=limit, author_id=author_id)
    return [BookResponse(**vars(b)) for b in books]


@router.post(
    "/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="書籍登録"
)
def create_book(
    data: BookCreate, use_case: BookUseCase = Depends(get_book_use_case)
) -> BookResponse:
    try:
        book = use_case.create_book(
            title=data.title,
            author_id=data.author_id,
            isbn=data.isbn,
            published_year=data.published_year,
            genre=data.genre,
            summary=data.summary,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return BookResponse(**vars(book))


@router.get("/{book_id}", response_model=BookResponse, summary="書籍取得")
def get_book(book_id: int, use_case: BookUseCase = Depends(get_book_use_case)) -> BookResponse:
    try:
        book = use_case.get_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return BookResponse(**vars(book))


@router.put("/{book_id}", response_model=BookResponse, summary="書籍更新")
def update_book(
    book_id: int, data: BookUpdate, use_case: BookUseCase = Depends(get_book_use_case)
) -> BookResponse:
    try:
        book = use_case.update_book(
            book_id,
            title=data.title,
            isbn=data.isbn,
            published_year=data.published_year,
            genre=data.genre,
            summary=data.summary,
            author_id=data.author_id,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return BookResponse(**vars(book))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="書籍削除")
def delete_book(book_id: int, use_case: BookUseCase = Depends(get_book_use_case)) -> None:
    try:
        use_case.delete_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
