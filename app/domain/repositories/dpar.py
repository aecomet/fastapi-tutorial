from abc import ABC, abstractmethod

from app.domain.entities.dpar import Dpar


class IDparRepository(ABC):
    @abstractmethod
    def get(self, key: str) -> Dpar | None: ...

    @abstractmethod
    def set(self, key: str, value: str, ttl: int | None = None) -> Dpar: ...

    @abstractmethod
    def delete(self, key: str) -> bool: ...

    @abstractmethod
    def keys(self, pattern: str = "*") -> list[str]: ...
