from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import health, root
from app.routers.health import set_startup_complete


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    set_startup_complete()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(root.router)
app.include_router(health.router)
