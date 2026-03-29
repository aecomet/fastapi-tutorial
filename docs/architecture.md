# アーキテクチャ

## 技術スタック

| 役割 | ツール | バージョン |
|------|--------|-----------|
| Web フレームワーク | FastAPI | >=0.135.2 |
| ASGI サーバー | Uvicorn | >=0.42.0 |
| データバリデーション・設定管理 | Pydantic / pydantic-settings | (FastAPI 依存 / >=2.13.1) |
| ORM | SQLAlchemy | >=2.0.48 |
| DB ドライバー | PyMySQL | >=1.1.2 |
| KV ストア・Pub/Sub | Redis | >=7.4.0 |
| コンテナ | Docker + Docker Compose | - |
| パッケージ管理 | uv | - |
| 言語 | Python | >=3.14 |
| Lint / Format | Ruff | >=0.15.8 |
| テスト | pytest / pytest-asyncio / fakeredis | >=9.0.2 |

## アーキテクチャ概要

**Clean Architecture** を採用。依存関係は外側から内側への一方向のみ許可する。

```
presentation ──→ application ──→ domain ←── infrastructure
```

| レイヤー | パス | 責務 | 外部依存 |
|---------|------|------|---------|
| **Domain** | `app/domain/` | エンティティ・リポジトリ抽象・例外定義 | なし（純粋 Python） |
| **Application** | `app/application/` | ユースケース（ビジネスロジック） | Domain のみ |
| **Infrastructure** | `app/infrastructure/` | DB・Redis の具体実装 | SQLAlchemy・redis-py |
| **Presentation** | `app/presentation/` | FastAPI ルーター・スキーマ | Application・Infrastructure |

## ディレクトリ構成

```
fastapi-tutorial/
├── .github/
│   ├── copilot-instructions.md          # Copilot 共通指示
│   └── instructions/
│       └── fastapi-review.instructions.md
│
├── app/
│   ├── main.py                          # FastAPI インスタンス・lifespan・ルーター登録・ログ設定
│   ├── middleware.py                    # ASGI リクエストログ（例外スタックトレース含む）
│   ├── logging_config.py               # RFC 7159 準拠 JsonFormatter
│   │
│   ├── config/                          # 環境別設定（pydantic-settings）
│   │   ├── base.py                      # 共通 Settings（database_url / redis_url / log_level）
│   │   ├── local.py                     # ローカル設定
│   │   ├── production.py               # 本番設定
│   │   ├── log_config.local.json       # ローカル用ログ設定
│   │   └── log_config.production.json  # 本番用ログ設定
│   │
│   ├── domain/                          # ドメイン層（外部依存なし）
│   │   ├── entities/
│   │   │   ├── author.py               # Author dataclass
│   │   │   ├── book.py                 # Book dataclass
│   │   │   └── dpar.py                 # Event dataclass
│   │   ├── repositories/
│   │   │   ├── author.py               # IAuthorRepository (ABC)
│   │   │   ├── book.py                 # IBookRepository (ABC)
│   │   │   └── dpar.py                 # IEventBus (ABC)
│   │   └── exceptions.py               # NotFoundError
│   │
│   ├── application/                     # アプリケーション層
│   │   └── use_cases/
│   │       ├── author.py               # AuthorUseCase
│   │       ├── book.py                 # BookUseCase
│   │       └── dpar.py                 # EventUseCase
│   │
│   ├── infrastructure/                  # インフラ層
│   │   ├── database.py                 # SQLAlchemy engine / SessionLocal / get_db()
│   │   ├── redis.py                    # get_redis()（同期/health用）・get_async_redis()（Pub/Sub用）
│   │   ├── models/
│   │   │   ├── author.py               # AuthorModel (ORM)
│   │   │   └── book.py                 # BookModel (ORM)
│   │   └── repositories/
│   │       ├── author.py               # SqlAlchemyAuthorRepository
│   │       ├── book.py                 # SqlAlchemyBookRepository
│   │       └── dpar.py                 # RedisEventBus（redis.asyncio）
│   │
│   └── presentation/                   # プレゼンテーション層
│       ├── schemas/
│       │   ├── author.py               # Pydantic スキーマ
│       │   ├── book.py
│       │   ├── dpar.py
│       │   └── root.py                 # RootResponse / ルート一覧
│       └── routers/
│           ├── v1/
│           │   ├── health.py           # GET /api/v1/health/*
│           │   └── root.py             # GET /api/v1/
│           ├── v2/
│           │   ├── authors.py          # CRUD /api/v2/authors
│           │   └── books.py            # CRUD /api/v2/books
│           └── v3/
│               └── dpar.py             # Pub/Sub /api/v3/dpar（publish のみ）
│
├── workers/                             # 非同期バックグラウンドワーカー
│   ├── base.py                         # BaseWorker（ABC）
│   └── dpar.py                         # EventWorker（Redis Subscribe → ログ出力）
│
├── tests/
│   ├── integration/
│   │   ├── test_root_endpoint.py       # v1 エンドポイント統合テスト
│   │   ├── test_v2_crud.py             # v2 CRUD 統合テスト
│   │   └── test_v3_dpar.py             # v3 dpar Publish 統合テスト
│   └── unit/
│       ├── test_event_worker.py        # EventWorker 単体テスト
│       ├── test_health_service.py
│       └── test_hello_service.py
│
├── docs/
│   └── architecture.md                 # このファイル
│                                        # ※ OpenAPI スキーマは /openapi.json で自動生成
│
├── Dockerfile
├── docker-compose.yml                  # api / mysql / redis サービス
├── main.py                             # エントリーポイント
├── pyproject.toml
└── README.md
```

## インフラ構成（Docker Compose）

```
クライアント
    │ HTTP :8000
    ▼
┌─────────────────────────────────────────────┐
│  api (FastAPI + Uvicorn)                    │
│  RequestLoggingMiddleware                   │
│    ├── /api/v1/*  → presentation/routers/v1 │
│    ├── /api/v2/*  → presentation/routers/v2 │
│    └── /api/v3/*  → presentation/routers/v3 │
│                                             │
│  EventWorker (asyncio.Task)                 │
│    └── Redis SUBSCRIBE → ログ出力           │
└──────────┬──────────────────┬───────────────┘
           │ MySQL :3306       │ Redis :6379
           ▼                  ▼
     ┌──────────┐       ┌──────────┐
     │  MySQL   │       │  Redis   │
     │  8.4     │       │  7       │
     └──────────┘       └──────────┘
```

## エンドポイント一覧

### v1 — システム

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v1/` | Hello World + ルート一覧 |
| GET | `/api/v1/health/startup` | K8s startupProbe（DB・Redis 疎通チェック含む） |
| GET | `/api/v1/health/readiness` | K8s readinessProbe |
| GET | `/api/v1/health/liveness` | K8s livenessProbe |

### v2 — Author / Book CRUD（MySQL）

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v2/authors/` | 著者一覧 |
| POST | `/api/v2/authors/` | 著者登録 |
| GET | `/api/v2/authors/{id}` | 著者取得 |
| PUT | `/api/v2/authors/{id}` | 著者更新 |
| DELETE | `/api/v2/authors/{id}` | 著者削除 |
| GET | `/api/v2/books/` | 書籍一覧（author_id フィルタ対応） |
| POST | `/api/v2/books/` | 書籍登録 |
| GET | `/api/v2/books/{id}` | 書籍取得 |
| PUT | `/api/v2/books/{id}` | 書籍更新 |
| DELETE | `/api/v2/books/{id}` | 書籍削除 |

### v3 — Dpar イベントバス（Redis Pub/Sub）

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v3/dpar/{channel}/publish` | チャンネルにイベントを Publish |

> **Subscribe はエンドポイントではなくバックグラウンドワーカーで処理する。**  
> `EventWorker` が `DPAR_WORKER_CHANNEL`（デフォルト: `events`）を Subscribe し、  
> 受信イベントをログ出力する。追加チャンネルを購読したい場合は `lifespan` にワーカーを追加する。


### API ドキュメント（自動生成）

| パス | 説明 |
|------|------|
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI スキーマ（JSON） |

> `docs/openapi.yaml` は管理しない。FastAPI が `/openapi.json` を常に最新状態で自動生成するため。

## リクエストフロー（v2 例）

```
POST /api/v2/authors/
  │
  ▼ RequestLoggingMiddleware（リクエストボディをログ出力）
  ▼ FastAPI ルーティング → presentation/routers/v2/authors.py
  ▼ get_author_use_case() DI
  ▼ AuthorUseCase.create_author()
  ▼ SqlAlchemyAuthorRepository.create()
  ▼ MySQL INSERT
  ▼ Author エンティティ → AuthorResponse スキーマ → JSON レスポンス
  ▼ RequestLoggingMiddleware（レスポンスステータスをログ出力）
```

## リクエストフロー（v3 dpar 例）

```
POST /api/v3/dpar/{channel}/publish
  │
  ▼ FastAPI ルーティング → presentation/routers/v3/dpar.py
  ▼ get_event_use_case() DI（get_async_redis → RedisEventBus）
  ▼ EventUseCase.publish(channel, payload)
  ▼ RedisEventBus.publish() → Redis PUBLISH
  ▼ EventResponse（channel / payload / event_id / timestamp）→ JSON

EventWorker（asyncio.Task、lifespan で起動）
  ▼ RedisEventBus.subscribe(channel) → Redis SUBSCRIBE
  ▼ 非同期ループでメッセージを受信
  ▼ logger.info("Event consumed", extra={channel, event_id, payload, timestamp})
```

## 環境設定

| 環境変数 | デフォルト | 説明 |
|---------|-----------|------|
| `APP_ENV` | `local` | 設定プロファイル（local / production） |
| `DATABASE_URL` | `sqlite:///./fastapi_dev.db` | MySQL 接続文字列 |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis 接続文字列 |
| `LOG_LEVEL` | `INFO` | ログレベル |
| `DPAR_WORKER_CHANNEL` | `events` | EventWorker が Subscribe するチャンネル名 |

## K8s Probe 設定例

```yaml
startupProbe:
  httpGet:
    path: /api/v1/health/startup
    port: 8000
  failureThreshold: 30
  periodSeconds: 5

readinessProbe:
  httpGet:
    path: /api/v1/health/readiness
    port: 8000
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /api/v1/health/liveness
    port: 8000
  periodSeconds: 30
```



