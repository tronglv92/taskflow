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

# The engine owns connection-pool configuration, not an active connection.
engine = create_engine(settings.database_url, connect_args=_connect_args, future=True)
# A factory rather than one global session: every request receives an isolated
# unit of work and cannot accidentally reuse another request's transaction.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
# Models inherit from Base. SQLAlchemy uses that shared metadata to discover
# the tables that ``init_db`` can create for a local database.
Base = declarative_base()


def get_db():
    """FastAPI dependency: yield one request-scoped session, then close it.

    FastAPI resumes this generator after the route returns *or* raises, so the
    ``finally`` block prevents checked-out connections from leaking on errors.
    """
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

    # ``create_all`` creates missing tables but cannot track schema history.
    # Alembic migrations, rather than this convenience method, evolve a real DB.
    Base.metadata.create_all(bind=engine)
