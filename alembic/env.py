from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Этот блок добавляется для импорта ваших моделей и используемой вами базы данных SQLAlchemy
import sys
import os

sys.path.append(os.getcwd())
from Home_work.app_main import db_users

# Это нужно для корректной работы Alembic
config = context.config
fileConfig(config.config_file_name)

# Укажите объект метаданных вашей базы данных SQLAlchemy
target_metadata = db_users.metadata

# Здесь необходимо передать объект метаданных в Alembic
config.set_main_option('sqlalchemy.url', str(db_users.engine.url))


def run_migrations_offline():
    """Эта функция применяет миграции в автономном режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Эта функция применяет миграции в режиме онлайн."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
