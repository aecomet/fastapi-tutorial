from collections.abc import AsyncIterator

from app.domain.entities.dpar import Event
from app.domain.repositories.dpar import IEventBus


class EventUseCase:
    def __init__(self, bus: IEventBus) -> None:
        self._bus = bus

    async def publish(self, channel: str, payload: dict) -> Event:
        return await self._bus.publish(channel, payload)

    def subscribe(self, channel: str) -> AsyncIterator[Event]:
        return self._bus.subscribe(channel)
