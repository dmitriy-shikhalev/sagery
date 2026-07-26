import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. Импортируем ваши Base и модели (как настроили ранее)
from sagery.db.base import Base
import sagery.models

# Объект конфигурации Alembic, предоставляющий доступ к значениям из alembic.ini
config = context.config

# Интерпретируем файл конфигурации для логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метадату ваших моделей для поддержки автогенерации (--autogenerate)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме (генерация SQL-скрипта в файл)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Синхронный помощник для применения миграций внутри async-соединения."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Создание асинхронного движка и запуск миграций."""
    # Извлекаем параметры подключения из секции [alembic] в alembic.ini
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # asyncpg требует выполнения синхронных команд Alembic через run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (прямое подключение к БД)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()  # Здесь должна вызываться ОНЛАЙН функция!