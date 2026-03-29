import logging

import redis.asyncio as aioredis

from app.application.use_cases.dapr import EventUseCase
from app.infrastructure.repositories.dapr import RedisEventBus
from app.workers.base import BaseWorker

logger = logging.getLogger(__name__)


class EventWorker(BaseWorker):
    """指定チャンネルを Subscribe し、受信イベントをログ出力するワーカー。

    サブクラスでチャンネルを固定する場合は channel をクラス属性として上書きする。
    """

    def __init__(self, channel: str, redis_client: aioredis.Redis) -> None:
        self._channel = channel
        self._redis_client = redis_client

    @property
    def channel(self) -> str:
        return self._channel

    async def _consume(self) -> None:
        use_case = EventUseCase(bus=RedisEventBus(self._redis_client))
        async for event in use_case.subscribe(self._channel):
            logger.info(
                "Event consumed",
                extra={
                    "channel": event.channel,
                    "event_id": event.event_id,
                    "payload": event.payload,
                    "timestamp": event.timestamp.isoformat(),
                },
            )
