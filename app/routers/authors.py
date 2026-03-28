from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import author as crud_author
from app.database import get_db
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["authors"])


def _get_or_404(author_id: int, db: Session) -> crud_author.Author:
    author = crud_author.get(db, author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.get("/", response_model=list[AuthorResponse], summary="著者一覧取得")
def list_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[crud_author.Author]:
    return crud_author.get_list(db, skip=skip, limit=limit)


@router.post(
    "/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED, summary="著者登録"
)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)) -> crud_author.Author:
    return crud_author.create(db, data)


@router.get("/{author_id}", response_model=AuthorResponse, summary="著者取得")
def get_author(author_id: int, db: Session = Depends(get_db)) -> crud_author.Author:
    return _get_or_404(author_id, db)


@router.put("/{author_id}", response_model=AuthorResponse, summary="著者更新")
def update_author(
    author_id: int, data: AuthorUpdate, db: Session = Depends(get_db)
) -> crud_author.Author:
    author = _get_or_404(author_id, db)
    return crud_author.update(db, author, data)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT, summary="著者削除")
def delete_author(author_id: int, db: Session = Depends(get_db)) -> None:
    author = _get_or_404(author_id, db)
    crud_author.delete(db, author)
