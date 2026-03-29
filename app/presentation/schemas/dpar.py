from datetime import datetime

from pydantic import BaseModel


class EventPublish(BaseModel):
    payload: dict


class EventResponse(BaseModel):
    channel: str
    payload: dict
    event_id: str
    timestamp: datetime
