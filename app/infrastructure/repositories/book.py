from sqlalchemy.orm import Session

from app.domain.entities.book import Book
from app.domain.repositories.book import IBookRepository
from app.infrastructure.models.book import BookModel


def _to_entity(model: BookModel) -> Book:
    return Book(
        id=model.id,
        title=model.title,
        isbn=model.isbn,
        published_year=model.published_year,
        genre=model.genre,
        summary=model.summary,
        author_id=model.author_id,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class SqlAlchemyBookRepository(IBookRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, book_id: int) -> Book | None:
        model = self._db.query(BookModel).filter(BookModel.id == book_id).first()
        return _to_entity(model) if model else None

    def get_list(
        self, skip: int = 0, limit: int = 100, author_id: int | None = None
    ) -> list[Book]:
        query = self._db.query(BookModel)
        if author_id is not None:
            query = query.filter(BookModel.author_id == author_id)
        return [_to_entity(m) for m in query.offset(skip).limit(limit).all()]

    def create(
        self,
        title: str,
        author_id: int,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
        summary: str | None = None,
    ) -> Book:
        model = BookModel(
            title=title,
            author_id=author_id,
            isbn=isbn,
            published_year=published_year,
            genre=genre,
            summary=summary,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def update(
        self,
        book: Book,
        title: str | None = None,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
        summary: str | None = None,
        author_id: int | None = None,
    ) -> Book:
        model = self._db.query(BookModel).filter(BookModel.id == book.id).first()
        for field, value in dict(
            title=title,
            isbn=isbn,
            published_year=published_year,
            genre=genre,
            summary=summary,
            author_id=author_id,
        ).items():
            if value is not None:
                setattr(model, field, value)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def delete(self, book: Book) -> None:
        model = self._db.query(BookModel).filter(BookModel.id == book.id).first()
        self._db.delete(model)
        self._db.commit()
