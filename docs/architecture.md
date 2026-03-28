# アーキテクチャ

## 技術スタック

| 役割 | ツール | バージョン |
|------|--------|-----------|
| Web フレームワーク | FastAPI | >=0.135.2 |
| ASGI サーバー | Uvicorn | >=0.42.0 |
| データバリデーション | Pydantic | (FastAPI 依存) |
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
