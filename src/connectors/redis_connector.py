import redis.asyncio as redis


class RedisManager:
    _redis: redis.Redis

    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def connect(self):
        """
        self.redis = None в начале потомучто мы не умеем объявлять асихронный redis
        :return:
        """
        self._redis = await redis.Redis(host=self.host, port=self.port)

    async def invalidate_book_cache(self):
        """Удаляем весь кэш, связанный с книгами"""
        deleted = 0

        # Удаляем кэш для отдельных книг и списков
        async for key in self._redis.scan_iter(match="fastapi-cache::books:*"):
            await self._redis.delete(key)
            deleted += 1

        async for key in self._redis.scan_iter(match="fastapi-cache::book:*"):
            await self._redis.delete(key)
            deleted += 1

        print(f"[Redis] Инвалидировано {deleted} ключей книг")  # для отладки

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        value = await self._redis.get(key)
        return value

    async def delete(self, key: str):
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
