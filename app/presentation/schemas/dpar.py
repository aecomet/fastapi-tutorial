from pydantic import BaseModel, Field


class DparSet(BaseModel):
    value: str
    ttl: int | None = Field(default=None, description="有効期限（秒）。省略時は無期限")


class DparResponse(BaseModel):
    key: str
    value: str
    ttl: int | None = Field(description="残り TTL（秒）。None は無期限")


class DparKeysResponse(BaseModel):
    keys: list[str]
    count: int
