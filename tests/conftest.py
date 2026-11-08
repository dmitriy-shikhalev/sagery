import pytest

from sagery.settings import Settings


@pytest.fixture(scope="session")
async def settings():
    return Settings()
