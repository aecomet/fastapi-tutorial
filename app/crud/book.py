from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def get(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def get_list(
    db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None
) -> list[Book]:
    query = db.query(Book)
    if author_id is not None:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create(db: Session, data: BookCreate) -> Book:
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update(db: Session, book: Book, data: BookUpdate) -> Book:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def delete(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
