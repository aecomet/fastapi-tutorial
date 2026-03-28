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
    RouteInfo(path="/api/v2/authors", method="GET", description="著者一覧取得"),
    RouteInfo(path="/api/v2/authors", method="POST", description="著者登録"),
    RouteInfo(path="/api/v2/authors/{id}", method="GET", description="著者取得"),
    RouteInfo(path="/api/v2/authors/{id}", method="PUT", description="著者更新"),
    RouteInfo(path="/api/v2/authors/{id}", method="DELETE", description="著者削除"),
    RouteInfo(path="/api/v2/books", method="GET", description="書籍一覧取得"),
    RouteInfo(path="/api/v2/books", method="POST", description="書籍登録"),
    RouteInfo(path="/api/v2/books/{id}", method="GET", description="書籍取得"),
    RouteInfo(path="/api/v2/books/{id}", method="PUT", description="書籍更新"),
    RouteInfo(path="/api/v2/books/{id}", method="DELETE", description="書籍削除"),
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
