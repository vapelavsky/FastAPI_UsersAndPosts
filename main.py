from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
import uvicorn
from fastapi_cache import FastAPICache, JsonCoder
from fastapi_cache.backends.inmemory import InMemoryBackend

from config import webserver_port, debug_mode_flag
from auth.endpoints import auth_router
from posts.endpoints import posts_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    FastAPICache.init(backend=InMemoryBackend(), prefix="fastapi-cache", coder=JsonCoder)


app.include_router(auth_router)
app.include_router(posts_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=webserver_port, reload=debug_mode_flag
    )
