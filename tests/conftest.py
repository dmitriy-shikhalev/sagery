import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine

from sagery.settings import Settings


@pytest.fixture(scope="session", autouse=True)
def migrate_database():
    # 1. Путь к конфигурации Alembic
    alembic_cfg = Config("alembic.ini")

    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

    # Передаем управление тестам
    yield


@pytest.fixture(scope="session")
async def settings():
    return Settings()


@pytest.fixture(scope="session")
async def engine(settings):
    async with create_async_engine(url=settings.postgres.url.unicode_string()):
        pass


@pytest.fixture()
def session():
    pass
