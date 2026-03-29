from abc import ABC, abstractmethod

from app.domain.entities.book import Book


class IBookRepository(ABC):
    @abstractmethod
    def get(self, book_id: int) -> Book | None: ...

    @abstractmethod
    def get_list(
        self, skip: int = 0, limit: int = 100, author_id: int | None = None
    ) -> list[Book]: ...

    @abstractmethod
    def create(
        self,
        title: str,
        author_id: int,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
        summary: str | None = None,
    ) -> Book: ...

    @abstractmethod
    def update(
        self,
        book: Book,
        title: str | None = None,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
        summary: str | None = None,
        author_id: int | None = None,
    ) -> Book: ...

    @abstractmethod
    def delete(self, book: Book) -> None: ...
