# fastapi-tutorial

FastAPI の学習用チュートリアルプロジェクトです。

## 必要条件

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## セットアップ

```bash
# リポジトリのクローン
git clone <repository-url>
cd fastapi-tutorial

# 依存パッケージのインストール（仮想環境も自動作成）
uv sync
```

## サーバー起動

```bash
uv run uvicorn main:app --reload
```

`--reload` オプションにより、コードの変更が自動的に反映されます。

## 動作確認

サーバー起動後、以下の方法で確認できます。

### curl

```bash
curl http://127.0.0.1:8000/
# => {"message":"Hello World"}
```

### ブラウザ

| URL | 内容 |
|-----|------|
| http://127.0.0.1:8000/ | Hello World API |
| http://127.0.0.1:8000/docs | Swagger UI（インタラクティブドキュメント） |
| http://127.0.0.1:8000/redoc | ReDoc（APIリファレンス） |

## テスト

```bash
uv run pytest -v
```

## パッケージ管理

```bash
# パッケージ追加
uv add <package-name>

# パッケージ削除
uv remove <package-name>
```

## プロジェクト構成

```
fastapi-tutorial/
├── .github/
│   ├── copilot-instructions.md      # Copilot 共通指示
│   └── instructions/                # パス別レビュー観点
├── app/
│   ├── main.py                      # FastAPI アプリ本体・lifespan 定義
│   ├── routers/
│   │   ├── root.py                  # GET / エンドポイント
│   │   └── health.py                # K8s ヘルスチェックエンドポイント
│   └── services/
│       └── hello.py                 # ビジネスロジック
├── docs/                            # アーキテクチャ・設計ドキュメント
├── tests/
│   ├── integration/                 # HTTP レイヤー統合テスト
│   └── unit/                        # 単体テスト
├── main.py                          # エントリーポイント（app.main に委譲）
├── pyproject.toml                   # プロジェクト設定・依存関係
├── uv.lock                          # 依存関係ロックファイル
└── README.md                        # このファイル
```
