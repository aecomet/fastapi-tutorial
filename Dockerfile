# ---- builder ----
FROM python:3.14-slim AS builder

WORKDIR /app

# uv をインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# 依存関係のみ先にコピーしてキャッシュを活かす
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ---- runtime ----
FROM python:3.14-slim AS runtime

WORKDIR /app

# 仮想環境をコピー
COPY --from=builder /app/.venv /app/.venv

# アプリケーションコードをコピー
COPY main.py ./
COPY app/ ./app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
