from sqlalchemy.orm import Session

from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


def get(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def get_list(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def create(db: Session, data: AuthorCreate) -> Author:
    author = Author(**data.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update(db: Session, author: Author, data: AuthorUpdate) -> Author:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    return author


def delete(db: Session, author: Author) -> None:
    db.delete(author)
    db.commit()
