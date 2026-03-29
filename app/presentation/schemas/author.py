from datetime import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None


class AuthorResponse(BaseModel):
    id: int
    name: str
    bio: str | None
    created_at: datetime
