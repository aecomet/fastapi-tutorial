from app.domain.entities.dpar import Dpar
from app.domain.exceptions import NotFoundError
from app.domain.repositories.dpar import IDparRepository


class DparUseCase:
    def __init__(self, repo: IDparRepository) -> None:
        self._repo = repo

    def get(self, key: str) -> Dpar:
        dpar = self._repo.get(key)
        if dpar is None:
            raise NotFoundError(f"key '{key}' not found")
        return dpar

    def set(self, key: str, value: str, ttl: int | None = None) -> Dpar:
        return self._repo.set(key, value, ttl=ttl)

    def delete(self, key: str) -> None:
        if not self._repo.delete(key):
            raise NotFoundError(f"key '{key}' not found")

    def keys(self, pattern: str = "*") -> list[str]:
        return self._repo.keys(pattern)
