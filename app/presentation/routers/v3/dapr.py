import redis.asyncio as aioredis
from fastapi import APIRouter, Depends

from app.application.use_cases.dapr import EventUseCase
from app.infrastructure.redis import get_async_redis
from app.infrastructure.repositories.dapr import RedisEventBus
from app.presentation.schemas.dapr import EventPublish, EventResponse

router = APIRouter(prefix="/dapr", tags=["dapr"])

# Redis Streams publish endpoint (統合)
@router.post(
    "/streams/{stream}/publish",
    response_model=dict,  # Streamsはevent_idのみ返す
    summary="Redis Streamsにイベント追加",
    description="指定ストリームにイベントをXADDで追加する。"
)
async def publish_stream_event(
    stream: str,
    data: EventPublish,
    redis: aioredis.Redis = Depends(get_async_redis),
):
    import json
    event_id = await redis.xadd(stream, {"payload": json.dumps(data.payload)})
    return {"stream": stream, "event_id": event_id}


def get_event_use_case(client: aioredis.Redis = Depends(get_async_redis)) -> EventUseCase:
    return EventUseCase(bus=RedisEventBus(client))


@router.post(
    "/{channel}/publish",
    response_model=EventResponse,
    summary="イベント発行",
    description="指定チャンネルにイベントを Publish する。",
)
async def publish_event(
    channel: str,
    data: EventPublish,
    use_case: EventUseCase = Depends(get_event_use_case),
) -> EventResponse:
    event = await use_case.publish(channel, data.payload)
    return EventResponse(
        channel=event.channel,
        payload=event.payload,
        event_id=event.event_id,
        timestamp=event.timestamp,
    )
