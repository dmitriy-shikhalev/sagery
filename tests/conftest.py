import pytest
from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session", autouse=True)
def migrate_database():
    # 1. Путь к конфигурации Alembic
    alembic_cfg = Config("alembic.ini")

    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

    # Передаем управление тестам
    yield
