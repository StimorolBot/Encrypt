import uvicorn
import asyncio
from fastapi import FastAPI

app = FastAPI(title="Encrypt")


@app.get("/")
async def hello_word():
    return "Hello Word"


async def main():
    config = uvicorn.Config(app="main:app", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(main())
