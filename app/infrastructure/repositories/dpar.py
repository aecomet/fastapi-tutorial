import redis

from app.domain.entities.dpar import Dpar
from app.domain.repositories.dpar import IDparRepository


class RedisDparRepository(IDparRepository):
    def __init__(self, client: redis.Redis) -> None:
        self._client = client

    def get(self, key: str) -> Dpar | None:
        value = self._client.get(key)
        if value is None:
            return None
        ttl = self._client.ttl(key)
        return Dpar(key=key, value=value, ttl=ttl if ttl >= 0 else None)

    def set(self, key: str, value: str, ttl: int | None = None) -> Dpar:
        if ttl is not None:
            self._client.setex(key, ttl, value)
        else:
            self._client.set(key, value)
        return Dpar(key=key, value=value, ttl=ttl)

    def delete(self, key: str) -> bool:
        return bool(self._client.delete(key))

    def keys(self, pattern: str = "*") -> list[str]:
        return [k for k in self._client.scan_iter(pattern)]
