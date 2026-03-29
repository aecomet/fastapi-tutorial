import asyncio
import json
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, call, patch

from app.workers.dapr import EventWorker


def make_redis_mock() -> MagicMock:
    return AsyncMock()


def test_event_worker_channel():
    """channel プロパティがコンストラクタで指定した値を返すこと"""
    worker = EventWorker(channel="test-ch", redis_client=make_redis_mock())
    assert worker.channel == "test-ch"


async def test_event_worker_run_logs_start():
    """run() が開始時に 'Worker started' をログ出力すること"""
    worker = EventWorker(channel="test-ch", redis_client=make_redis_mock())

    async def fake_consume() -> None:
        pass

    with patch("app.workers.base.logger") as mock_logger:
        with patch.object(worker, "_consume", new=fake_consume):
            await worker.run()

    mock_logger.info.assert_called_once_with("Worker started", extra={"channel": "test-ch"})


async def test_event_worker_run_logs_stop_on_cancel():
    """run() がキャンセルされたとき 'Worker stopped' をログ出力すること"""
    worker = EventWorker(channel="test-ch", redis_client=make_redis_mock())

    async def fake_consume() -> None:
        await asyncio.sleep(10)

    with patch("app.workers.base.logger") as mock_logger:
        with patch.object(worker, "_consume", new=fake_consume):
            task = asyncio.create_task(worker.run())
            await asyncio.sleep(0)
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    mock_logger.info.assert_has_calls(
        [
            call("Worker started", extra={"channel": "test-ch"}),
            call("Worker stopped", extra={"channel": "test-ch"}),
        ]
    )


async def test_event_worker_logs_consumed_event():
    """メッセージを受信したとき 'Event consumed' をログ出力すること"""
    import fakeredis.aioredis

    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    worker = EventWorker(channel="test-ch", redis_client=client)

    with patch("app.workers.dapr.logger") as mock_logger:
        task = asyncio.create_task(worker.run())
        await asyncio.sleep(0.05)

        event_id = str(uuid.uuid4())
        message = json.dumps(
            {
                "event_id": event_id,
                "timestamp": datetime.now(UTC).isoformat(),
                "payload": {"key": "value"},
            }
        )
        await client.publish("test-ch", message)
        await asyncio.sleep(0.05)

        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

    await client.aclose()

    mock_logger.info.assert_called_once()
    _, kwargs = mock_logger.info.call_args
    assert kwargs["extra"]["channel"] == "test-ch"
    assert kwargs["extra"]["event_id"] == event_id
    assert kwargs["extra"]["payload"] == {"key": "value"}
