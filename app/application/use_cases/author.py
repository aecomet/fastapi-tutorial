from app.domain.entities.author import Author
from app.domain.exceptions import NotFoundError
from app.domain.repositories.author import IAuthorRepository


class AuthorUseCase:
    def __init__(self, repo: IAuthorRepository) -> None:
        self._repo = repo

    def list_authors(self, skip: int = 0, limit: int = 100) -> list[Author]:
        return self._repo.get_list(skip=skip, limit=limit)

    def get_author(self, author_id: int) -> Author:
        author = self._repo.get(author_id)
        if author is None:
            raise NotFoundError(f"Author id={author_id} not found")
        return author

    def create_author(self, name: str, bio: str | None = None) -> Author:
        return self._repo.create(name=name, bio=bio)

    def update_author(
        self, author_id: int, name: str | None = None, bio: str | None = None
    ) -> Author:
        author = self.get_author(author_id)
        return self._repo.update(author, name=name, bio=bio)

    def delete_author(self, author_id: int) -> None:
        author = self.get_author(author_id)
        self._repo.delete(author)
