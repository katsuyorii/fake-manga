from redis.asyncio import Redis

from src.redis import redis_client


async def get_redis() -> Redis:
    yield redis_client