import redis.asyncio as aioredis
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.application.use_cases.dpar import EventUseCase
from app.infrastructure.redis import get_async_redis
from app.infrastructure.repositories.dpar import RedisEventBus
from app.presentation.schemas.dpar import EventPublish, EventResponse

router = APIRouter(prefix="/dpar", tags=["dpar"])


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


@router.get(
    "/{channel}/subscribe",
    summary="イベント購読（SSE）",
    description="指定チャンネルを Subscribe し、SSE でイベントをストリーミングする。",
)
async def subscribe_events(
    channel: str,
    use_case: EventUseCase = Depends(get_event_use_case),
) -> StreamingResponse:
    async def event_stream():
        async for event in use_case.subscribe(channel):
            data = EventResponse(
                channel=event.channel,
                payload=event.payload,
                event_id=event.event_id,
                timestamp=event.timestamp,
            )
            yield f"data: {data.model_dump_json()}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
