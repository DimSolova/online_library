from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.books import router as router_books
from src.api.favorites import router as router_favorites
from src.api.reviews import router as router_reviews
from src.api.users import router as router_users
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    До yield будет выполняться код при запуске приложения,
    После yield его закрытие или например какое-то редактирование приложения
    """
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager), prefix="fastapi-cache")

    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_books)
app.include_router(router_reviews)
app.include_router(router_favorites)

if __name__ == "__main__":
    uvicorn.run(app)
