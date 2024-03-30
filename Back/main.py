import uvicorn
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi.staticfiles import StaticFiles
from fastapi_cache.backends.redis import RedisBackend

from core.config import redis
from src.app.encrypt.router.api_v1.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Encrypt")
app.include_router(router)
app.mount("/", StaticFiles(directory="../Front/"), name="css", )


async def main():
    config = uvicorn.Config(app="main:app", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(main())
