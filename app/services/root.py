from pydantic import BaseModel


class RouteInfo(BaseModel):
    path: str
    method: str
    description: str


class RootResponse(BaseModel):
    message: str
    routes: list[RouteInfo]


ROUTES: list[RouteInfo] = [
    RouteInfo(path="/api/v1/", method="GET", description="このページ"),
    RouteInfo(path="/api/v1/health/startup", method="GET", description="K8s startupProbe"),
    RouteInfo(path="/api/v1/health/readiness", method="GET", description="K8s readinessProbe"),
    RouteInfo(path="/api/v1/health/liveness", method="GET", description="K8s livenessProbe"),
    RouteInfo(
        path="/docs",
        method="GET",
        description="Swagger UI（インタラクティブ API ドキュメント）",
    ),
    RouteInfo(path="/redoc", method="GET", description="ReDoc（API リファレンス）"),
    RouteInfo(path="/openapi.json", method="GET", description="OpenAPI スキーマ"),
]


def build_root_response() -> RootResponse:
    return RootResponse(message="Hello World", routes=ROUTES)
