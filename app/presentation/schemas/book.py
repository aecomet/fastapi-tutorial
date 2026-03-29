from datetime import datetime

from pydantic import BaseModel


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


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str | None
    published_year: int | None
    genre: str | None
    summary: str | None
    author_id: int
    created_at: datetime
    updated_at: datetime
