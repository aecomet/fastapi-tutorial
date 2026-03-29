from dataclasses import dataclass
from datetime import datetime


@dataclass
class Author:
    id: int
    name: str
    bio: str | None
    created_at: datetime
