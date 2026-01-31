import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db.base import Base  # noqa

# Alembic Config object
config = context.config

# Logging
fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata

# ===============================
# Database URL from ENV
# ===============================
def get_url() -> str:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    host = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


# ===============================
# Offline migrations
# ===============================
def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ===============================
# Online migrations
# ===============================
def run_migrations_online():
    config_section = config.get_section(config.config_ini_section)
    config_section["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ===============================
# Run the right mode
# ===============================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
