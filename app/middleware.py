import logging

from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger("app.access")


class RequestLoggingMiddleware:
    """リクエストのクエリパラメーターとボディを構造化ログで出力する ASGI ミドルウェア。

    BaseHTTPMiddleware はボディを読み取るとストリームを消費してしまうため、
    receive / send を直接ラップする方式で実装している。
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "")
        path = scope.get("path", "")
        query_string = scope.get("query_string", b"").decode()
        query = dict(q.split("=", 1) for q in query_string.split("&") if "=" in q)

        body_parts: list[bytes] = []

        async def buffered_receive() -> dict:
            """ボディを読みながら下流に同じメッセージをそのまま渡す。"""
            message = await receive()
            if message["type"] == "http.request":
                body_parts.append(message.get("body", b""))
                if not message.get("more_body", False):
                    full_body = b"".join(body_parts)
                    body_str = full_body.decode("utf-8", errors="replace") if full_body else None
                    logger.info(
                        "request",
                        extra={
                            "http.method": method,
                            "http.path": path,
                            "http.query": query or None,
                            "http.request_body": body_str,
                        },
                    )
            return message

        async def logging_send(message: dict) -> None:
            if message["type"] == "http.response.start":
                logger.info(
                    "response",
                    extra={
                        "http.method": method,
                        "http.path": path,
                        "http.status_code": message["status"],
                    },
                )
            await send(message)

        await self.app(scope, buffered_receive, logging_send)
