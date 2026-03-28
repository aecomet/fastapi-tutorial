# アーキテクチャ

## 技術スタック

| 役割 | ツール | バージョン |
|------|--------|-----------|
| Web フレームワーク | FastAPI | >=0.135.2 |
| ASGI サーバー | Uvicorn | >=0.42.0 |
| データバリデーション | Pydantic | (FastAPI 依存) |
| コンテナ | Docker + Docker Compose | - |
| パッケージ管理 | uv | - |
| 言語 | Python | >=3.14 |
| Lint / Format | Ruff | >=0.15.8 |
| テスト | pytest + httpx | >=9.0.2 |

## コンポーネント構成

```
クライアント (ブラウザ / curl / K8s probe)
        │
        │ HTTP
        ▼
┌───────────────────┐
│    Docker         │  コンテナランタイム
│  (ポート 8000)    │  ホスト ↔ コンテナのポートマッピング
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│    Uvicorn        │  ASGI サーバー
│                   │  リクエストの受付・プロセス管理
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│    FastAPI        │  Web フレームワーク
│    (Starlette)    │  ルーティング・バリデーション・シリアライズ
└────────┬──────────┘
         │
         ├─── app/routers/root.py      # / エンドポイント
         ├─── app/routers/health.py    # /health/* エンドポイント
         │
         ▼
┌───────────────────┐
│  app/services/    │  ビジネスロジック層
│                   │  サービス関数（ルーターから呼び出し）
└───────────────────┘
```

## ディレクトリ構成

```
fastapi-tutorial/
├── .github/
│   ├── copilot-instructions.md      # Copilot 共通指示（diff確認・Conventional Commits 等）
│   └── instructions/
│       └── fastapi-review.instructions.md  # *.py へのレビュー観点
│
├── app/                             # アプリケーション本体
│   ├── __init__.py
│   ├── main.py                      # FastAPI インスタンス生成・lifespan・ルーター登録
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── root.py                  # GET /
│   │   └── health.py                # GET /health/{startup,readiness,liveness}
│   └── services/
│       ├── __init__.py
│       ├── root.py                  # RootResponse モデル・ルート一覧
│       └── hello.py                 # ビジネスロジック
│
├── docs/
│   ├── architecture.md              # このファイル（アーキテクチャ・構成の統合ドキュメント）
│   └── openapi.yaml                 # OpenAPI 3.1.0 スキーマ
│
├── tests/
│   ├── integration/
│   │   └── test_root_endpoint.py    # HTTP レイヤー統合テスト
│   └── unit/
│       ├── test_hello_service.py    # root サービス単体テスト
│       └── test_health_service.py   # health サービス単体テスト
│
├── Dockerfile                       # マルチステージビルド（builder / runtime）
├── docker-compose.yml               # prod（デフォルト）/ dev プロファイル
├── .dockerignore
├── main.py                          # エントリーポイント（app.main:app に委譲）
├── pyproject.toml                   # プロジェクト設定・依存関係・ruff/pytest 設定
├── uv.lock                          # 依存関係ロックファイル
└── README.md                        # セットアップ・起動手順
```

## 各レイヤーの責務

| レイヤー | パス | 責務 |
|---------|------|------|
| エントリーポイント | `main.py` | uvicorn 向けの `app` オブジェクト公開 |
| アプリ初期化 | `app/main.py` | FastAPI インスタンス・lifespan・ルーター登録 |
| ルーター | `app/routers/` | HTTP メソッド・パスの定義、レスポンス型の指定 |
| サービス | `app/services/` | ビジネスロジック（ルーターから呼び出す） |
| テスト | `tests/` | unit（サービス単体）/ integration（HTTP レイヤー） |
| ドキュメント | `docs/` | アーキテクチャ・API スキーマ |
| Copilot 設定 | `.github/` | instructions・レビュー観点 |

## リクエストフロー

### 通常リクエスト

```
GET /
  │
  ▼ Docker ポートマッピング (8000 → 8000)
  ▼ Uvicorn 受信
  ▼ FastAPI ルーティング → root.router
  ▼ read_root() 呼び出し
  ▼ build_root_response() (services/root.py)
  ▼ {"message": "Hello World", "routes": [...]} を JSON で返却
```

### K8s ヘルスチェック

```
GET /health/startup    → lifespan 完了後に 200、未完了時は 503
GET /health/readiness  → 常時 200（依存サービスが追加されたら要拡張）
GET /health/liveness   → 常時 200（プロセス生存確認）
```

## エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | Hello World + ルート一覧 |
| GET | `/health/startup` | K8s startupProbe 用 |
| GET | `/health/readiness` | K8s readinessProbe 用 |
| GET | `/health/liveness` | K8s livenessProbe 用 |
| GET | `/docs` | Swagger UI（自動生成） |
| GET | `/redoc` | ReDoc（自動生成） |
| GET | `/openapi.json` | OpenAPI スキーマ（自動生成） |

## K8s Probe 設定例

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8000
  failureThreshold: 30
  periodSeconds: 5

readinessProbe:
  httpGet:
    path: /health/readiness
    port: 8000
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /health/liveness
    port: 8000
  periodSeconds: 30
```

## 起動方法

| 環境 | コマンド | 特徴 |
|------|---------|------|
| 本番 | `docker compose up -d` | ビルド済みイメージで起動 |
| 開発 | `docker compose --profile dev up api-dev` | ホットリロード・ボリュームマウント |
| ローカル | `uv run uvicorn main:app --reload` | Docker 不要 |


## コンポーネント構成

```
クライアント (ブラウザ / curl / K8s probe)
        │
        │ HTTP
        ▼
┌───────────────────┐
│    Uvicorn        │  ASGI サーバー
│  (ポート 8000)    │  リクエストの受付・プロセス管理
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│    FastAPI        │  Web フレームワーク
│    (Starlette)    │  ルーティング・バリデーション・シリアライズ
└────────┬──────────┘
         │
         ├─── app/routers/root.py      # / エンドポイント
         ├─── app/routers/health.py    # /health/* エンドポイント
         │
         ▼
┌───────────────────┐
│  app/services/    │  ビジネスロジック層
│  hello.py         │  サービス関数（ルーターから呼び出し）
└───────────────────┘
```

## ファイル構成

→ 詳細は [project-structure.md](./project-structure.md) を参照。

## リクエストフロー

### 通常リクエスト

```
GET /
  │
  ▼ Uvicorn 受信
  ▼ FastAPI ルーティング → root.router
  ▼ read_root() 呼び出し
  ▼ build_hello_message() (services/hello.py)
  ▼ {"message": "Hello World"} を JSON で返却
```

### K8s ヘルスチェック

```
GET /health/startup    → lifespan 完了後に 200、未完了時は 503
GET /health/readiness  → 常時 200（依存サービスが追加されたら要拡張）
GET /health/liveness   → 常時 200（プロセス生存確認）
```

## エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | Hello World レスポンスを返す |
| GET | `/health/startup` | K8s startupProbe 用 |
| GET | `/health/readiness` | K8s readinessProbe 用 |
| GET | `/health/liveness` | K8s livenessProbe 用 |
| GET | `/docs` | Swagger UI（自動生成） |
| GET | `/redoc` | ReDoc（自動生成） |
| GET | `/openapi.json` | OpenAPI スキーマ（自動生成） |

## K8s Probe 設定例

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8000
  failureThreshold: 30
  periodSeconds: 5

readinessProbe:
  httpGet:
    path: /health/readiness
    port: 8000
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /health/liveness
    port: 8000
  periodSeconds: 30
```

## 開発サーバーとプロダクション

| 項目 | 開発 | プロダクション（例） |
|------|------|-----------------|
| 起動コマンド | `uv run uvicorn main:app --reload` | `uvicorn main:app --host 0.0.0.0 --workers 4` |
| ホットリロード | あり | なし |
| ワーカー数 | 1 | CPU コア数に応じて設定 |
