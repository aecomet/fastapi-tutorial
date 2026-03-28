from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import authors, books, health, root
from app.routers.health import set_startup_complete


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    Base.metadata.create_all(bind=engine)
    set_startup_complete()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(root.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(authors.router, prefix="/api/v2")
app.include_router(books.router, prefix="/api/v2")
