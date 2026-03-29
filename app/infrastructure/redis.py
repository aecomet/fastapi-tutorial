import redis
import redis.asyncio as aioredis

from app.config import get_settings

_settings = get_settings()


def get_redis() -> redis.Redis:  # type: ignore[override]
    """FastAPI Depends 用 同期 Redis クライアント（health check 用）。"""
    client = redis.Redis.from_url(_settings.redis_url, decode_responses=True)
    try:
        yield client
    finally:
        client.close()


async def get_async_redis():  # type: ignore[return]
    """FastAPI Depends 用 非同期 Redis クライアント（Pub/Sub 用）。"""
    client = aioredis.Redis.from_url(_settings.redis_url, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()
