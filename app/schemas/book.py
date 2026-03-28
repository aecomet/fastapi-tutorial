from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.author import AuthorResponse


class BookBase(BaseModel):
    title: str
    isbn: str | None = None
    published_year: int | None = None
    genre: str | None = None
    summary: str | None = None
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = None
    published_year: int | None = None
    genre: str | None = None
    summary: str | None = None
    author_id: int | None = None


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    author: AuthorResponse
