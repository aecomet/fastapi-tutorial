from abc import ABC, abstractmethod

from app.domain.entities.author import Author


class IAuthorRepository(ABC):
    @abstractmethod
    def get(self, author_id: int) -> Author | None: ...

    @abstractmethod
    def get_list(self, skip: int = 0, limit: int = 100) -> list[Author]: ...

    @abstractmethod
    def create(self, name: str, bio: str | None) -> Author: ...

    @abstractmethod
    def update(
        self, author: Author, name: str | None = None, bio: str | None = None
    ) -> Author: ...

    @abstractmethod
    def delete(self, author: Author) -> None: ...
