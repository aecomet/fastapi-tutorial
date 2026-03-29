from app.domain.entities.book import Book
from app.domain.exceptions import NotFoundError
from app.domain.repositories.author import IAuthorRepository
from app.domain.repositories.book import IBookRepository


class BookUseCase:
    def __init__(self, repo: IBookRepository, author_repo: IAuthorRepository) -> None:
        self._repo = repo
        self._author_repo = author_repo

    def list_books(
        self, skip: int = 0, limit: int = 100, author_id: int | None = None
    ) -> list[Book]:
        return self._repo.get_list(skip=skip, limit=limit, author_id=author_id)

    def get_book(self, book_id: int) -> Book:
        book = self._repo.get(book_id)
        if book is None:
            raise NotFoundError(f"Book id={book_id} not found")
        return book

    def create_book(
        self,
        title: str,
        author_id: int,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
        summary: str | None = None,
    ) -> Book:
        if self._author_repo.get(author_id) is None:
            raise NotFoundError(f"Author id={author_id} not found")
        return self._repo.create(
            title=title,
            author_id=author_id,
            isbn=isbn,
            published_year=published_year,
            genre=genre,
            summary=summary,
        )

    def update_book(
        self,
        book_id: int,
        title: str | None = None,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
        summary: str | None = None,
        author_id: int | None = None,
    ) -> Book:
        book = self.get_book(book_id)
        if author_id is not None and self._author_repo.get(author_id) is None:
            raise NotFoundError(f"Author id={author_id} not found")
        return self._repo.update(
            book,
            title=title,
            isbn=isbn,
            published_year=published_year,
            genre=genre,
            summary=summary,
            author_id=author_id,
        )

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        self._repo.delete(book)
