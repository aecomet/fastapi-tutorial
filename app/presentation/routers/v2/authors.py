from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.use_cases.author import AuthorUseCase
from app.domain.exceptions import NotFoundError
from app.infrastructure.database import get_db
from app.infrastructure.repositories.author import SqlAlchemyAuthorRepository
from app.presentation.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["authors"])


def get_author_use_case(db: Session = Depends(get_db)) -> AuthorUseCase:
    return AuthorUseCase(repo=SqlAlchemyAuthorRepository(db))


@router.get("/", response_model=list[AuthorResponse], summary="著者一覧取得")
def list_authors(
    skip: int = 0,
    limit: int = 100,
    use_case: AuthorUseCase = Depends(get_author_use_case),
) -> list[AuthorResponse]:
    authors = use_case.list_authors(skip=skip, limit=limit)
    return [AuthorResponse(**vars(a)) for a in authors]


@router.post(
    "/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED, summary="著者登録"
)
def create_author(
    data: AuthorCreate, use_case: AuthorUseCase = Depends(get_author_use_case)
) -> AuthorResponse:
    author = use_case.create_author(name=data.name, bio=data.bio)
    return AuthorResponse(**vars(author))


@router.get("/{author_id}", response_model=AuthorResponse, summary="著者取得")
def get_author(
    author_id: int, use_case: AuthorUseCase = Depends(get_author_use_case)
) -> AuthorResponse:
    try:
        author = use_case.get_author(author_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return AuthorResponse(**vars(author))


@router.put("/{author_id}", response_model=AuthorResponse, summary="著者更新")
def update_author(
    author_id: int,
    data: AuthorUpdate,
    use_case: AuthorUseCase = Depends(get_author_use_case),
) -> AuthorResponse:
    try:
        author = use_case.update_author(author_id, name=data.name, bio=data.bio)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return AuthorResponse(**vars(author))


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT, summary="著者削除")
def delete_author(
    author_id: int, use_case: AuthorUseCase = Depends(get_author_use_case)
) -> None:
    try:
        use_case.delete_author(author_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
