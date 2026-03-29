import json
from collections.abc import AsyncIterator
from datetime import datetime

import redis.asyncio as aioredis

from app.domain.entities.dpar import Event
from app.domain.repositories.dpar import IEventBus


class RedisEventBus(IEventBus):
    def __init__(self, client: aioredis.Redis) -> None:
        self._client = client

    async def publish(self, channel: str, payload: dict) -> Event:
        event = Event(channel=channel, payload=payload)
        message = json.dumps(
            {
                "event_id": event.event_id,
                "timestamp": event.timestamp.isoformat(),
                "payload": event.payload,
            }
        )
        await self._client.publish(channel, message)
        return event

    async def subscribe(self, channel: str) -> AsyncIterator[Event]:  # type: ignore[override]
        pubsub = self._client.pubsub()
        await pubsub.subscribe(channel)
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    data = json.loads(message["data"])
                    yield Event(
                        channel=channel,
                        payload=data["payload"],
                        event_id=data["event_id"],
                        timestamp=datetime.fromisoformat(data["timestamp"]),
                    )
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.aclose()
