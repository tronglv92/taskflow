"""Alembic migration environment."""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Make the app importable (it holds database.py, models.py). In the source tree
# that is ../app; in the container image the app/ contents are flattened onto the
# working directory, so fall back to the parent directory itself.
_here = os.path.dirname(os.path.abspath(__file__))
for _candidate in (os.path.join(os.path.dirname(_here), "app"), os.path.dirname(_here)):
    if os.path.isfile(os.path.join(_candidate, "database.py")):
        sys.path.insert(0, _candidate)
        break

from database import Base  # noqa: E402
import models  # noqa: E402,F401  (registers tables on Base.metadata)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# DATABASE_URL wins over anything in alembic.ini.
_db_url = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")
config.set_main_option("sqlalchemy.url", _db_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=_db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
