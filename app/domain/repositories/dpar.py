from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.domain.entities.dpar import Event


class IEventBus(ABC):
    @abstractmethod
    async def publish(self, channel: str, payload: dict) -> Event: ...

    @abstractmethod
    def subscribe(self, channel: str) -> AsyncIterator[Event]: ...
