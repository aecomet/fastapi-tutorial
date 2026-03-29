import redis

from app.config import get_settings

_settings = get_settings()


def get_redis() -> redis.Redis:
    """FastAPI Depends 用 Redis クライアントジェネレーター。"""
    client = redis.Redis.from_url(_settings.redis_url, decode_responses=True)
    try:
        yield client
    finally:
        client.close()
