from aioredis import Redis
from typing import Optional


redis: Optional[Redis] = None

async def get_redis() -> Optional[Redis]:
    return redis
