# プロジェクト構成

## ディレクトリ構成

```
fastapi-tutorial/
├── .github/
│   ├── copilot-instructions.md      # Copilot 共通指示（commit/push禁止・diff確認・Conventional Commits 等）
│   └── instructions/
│       └── fastapi-review.instructions.md  # *.py へのレビュー観点（format/lint/test/FastAPI規約）
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
│       └── hello.py                 # ビジネスロジック（build_hello_message）
│
├── docs/
│   ├── architecture.md              # システム構成・技術スタック・リクエストフロー
│   ├── project-structure.md         # このファイル
│   └── openapi.yaml                 # OpenAPI 3.1.0 スキーマ（Swagger 形式）
│
├── tests/
│   ├── integration/
│   │   └── test_root_endpoint.py    # HTTP レイヤー統合テスト（TestClient）
│   └── unit/
│       ├── test_hello_service.py    # hello サービス単体テスト
│       └── test_health_service.py   # health サービス単体テスト
│
├── main.py                          # エントリーポイント（app.main:app に委譲）
├── pyproject.toml                   # プロジェクト設定・依存関係・ruff/pytest 設定
├── uv.lock                          # 再現性確保のための依存ロックファイル
└── README.md                        # セットアップ・起動・動作確認手順
```

## 各レイヤーの責務

| レイヤー | ディレクトリ | 責務 |
|---------|-------------|------|
| エントリーポイント | `main.py` | uvicorn 向けの `app` オブジェクト公開 |
| アプリ初期化 | `app/main.py` | FastAPI インスタンス・lifespan・ルーター登録 |
| ルーター | `app/routers/` | HTTP メソッド・パスの定義、レスポンス型の指定 |
| サービス | `app/services/` | ビジネスロジック（ルーターから呼び出す） |
| テスト | `tests/` | unit（サービス単体）/ integration（HTTP レイヤー） |
| ドキュメント | `docs/` | アーキテクチャ・API スキーマ・本ファイル |
| CI 設定 | `.github/` | Copilot instructions・レビュー観点 |

## 設定ファイル

| ファイル | 内容 |
|---------|------|
| `pyproject.toml` | 依存関係・ruff（lint/format）・pytest（testpaths, pythonpath）設定 |
| `uv.lock` | 全依存パッケージのバージョンロック（`uv sync` で再現） |
| `.python-version` | プロジェクトで使用する Python バージョン固定 |
