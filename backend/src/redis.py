from redis.asyncio import Redis

from .settings import redis_settings


redis_client = Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, max_connections=redis_settings.REDIS_POOL_SIZE)