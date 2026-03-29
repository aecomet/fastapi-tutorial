import json
import logging
import traceback
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    """RFC 7159 準拠の JSON ログフォーマッター。

    各ログレコードを 1 行の JSON オブジェクトとして出力する。
    """

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            payload["exception"] = "".join(traceback.format_exception(*record.exc_info))

        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)

        # ミドルウェアが extra で渡した追加フィールドをそのままマージ
        for key, value in record.__dict__.items():
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "taskName",
                "message",
            }:
                payload[key] = value

        return json.dumps(payload, ensure_ascii=False)
