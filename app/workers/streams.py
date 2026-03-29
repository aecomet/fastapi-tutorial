import asyncio
import logging

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class StreamWorker:
    def __init__(self, stream: str, redis_client: Redis):
        self.stream = stream
        self.redis = redis_client
        self._running = True

    async def run(self):
        logger.info(f"StreamWorker started for stream: {self.stream}")
        last_id = "$"
        while self._running:
            try:
                response = await self.redis.xread({self.stream: last_id}, block=1000, count=1)
                if response:
                    for stream_name, messages in response:
                        for msg_id, msg in messages:
                            logger.info(
    f"[StreamWorker] Consumed from {stream_name}: "
    f"id={msg_id}, data={msg}"
)
                            last_id = msg_id
            except asyncio.CancelledError:
                logger.info("StreamWorker cancelled.")
                break
            except Exception as e:
                logger.error(f"StreamWorker error: {e}")
                await asyncio.sleep(1)

    def stop(self):
        self._running = False
