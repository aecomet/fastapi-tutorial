from dataclasses import dataclass
from datetime import datetime


@dataclass
class Book:
    id: int
    title: str
    isbn: str | None
    published_year: int | None
    genre: str | None
    summary: str | None
    author_id: int
    created_at: datetime
    updated_at: datetime
