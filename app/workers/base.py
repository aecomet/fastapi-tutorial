import asyncio
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseWorker(ABC):
    @property
    @abstractmethod
    def channel(self) -> str: ...

    async def run(self) -> None:
        logger.info("Worker started", extra={"channel": self.channel})
        try:
            await self._consume()
        except asyncio.CancelledError:
            logger.info("Worker stopped", extra={"channel": self.channel})
            raise

    @abstractmethod
    async def _consume(self) -> None: ...
