"""Database connection setup.

Exposes the SQLAlchemy ``engine``, a ``SessionLocal`` factory, the declarative
``Base``, and the ``get_db`` dependency used by routes.

``create_engine`` does not open a connection: the pool connects lazily on first
use. Nothing here touches the database at import time, so ``import app.main``
never needs a running database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

# SQLite needs check_same_thread=False when used from FastAPI's threadpool.
_connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(settings.database_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables for any model imported by the time this is called.

    Called from the FastAPI startup event, never at import time. In production
    Alembic migrations are the source of truth; this keeps local/SQLite runs
    working without a migration step.
    """
    import models  # noqa: F401  (registers models on Base.metadata)

    Base.metadata.create_all(bind=engine)
