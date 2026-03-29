from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

_settings = get_settings()
DATABASE_URL = _settings.database_url

# SQLite の場合は check_same_thread を無効化
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Session:
    """FastAPI Depends 用 DB セッションジェネレーター。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
