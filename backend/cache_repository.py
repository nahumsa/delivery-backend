import redis
import json
from config import settings


class CacheRepository:
    def __init__(self):
        self.client = redis.Redis(host=settings.redis_host, port=6379, db=0)

    def get(self, key: str):
        cached_data = self.client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def set(self, key: str, value: dict, ex: int):
        self.client.set(key, json.dumps(value), ex=ex)
