import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Event:
    channel: str
    payload: dict
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
