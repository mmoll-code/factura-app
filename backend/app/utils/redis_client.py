import redis.asyncio as redis
from app.core import config

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(config.REDIS_URL, decode_responses=True)
    return redis_client 