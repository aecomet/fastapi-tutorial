from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None


class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
