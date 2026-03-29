# fastapi-tutorial

FastAPI の学習用チュートリアルプロジェクトです。

## 必要条件

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose

## セットアップ

```bash
git clone <repository-url>
cd fastapi-tutorial
```

## サーバー起動

```bash
docker compose up
```

ホットリロード対応のため、コードの変更は自動的に反映されます。

> **依存パッケージを変更した場合は再ビルドが必要です**
> ```bash
> docker compose build
> docker compose up
> ```

## 動作確認

```bash
curl http://127.0.0.1:8000/
```

| URL | 内容 |
|-----|------|
| http://127.0.0.1:8000/ | Hello World + ルート一覧 |
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |

## テスト

```bash
# ローカル実行（uv が必要）
uv run pytest -v
```

## パッケージ管理

```bash
uv add <package-name>
uv remove <package-name>
```

## ドキュメント

- [アーキテクチャ・プロジェクト構成](docs/architecture.md)
- [OpenAPI スキーマ](docs/openapi.yaml)

