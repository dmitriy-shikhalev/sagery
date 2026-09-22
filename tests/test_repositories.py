from unittest.mock import Mock

import pytest
from mypy.typeanal import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from sagery.repositories import AbstractRepository, SagaRepository


@pytest.mark.parametrize(
    ["klass"],
    [
        (SagaRepository,),
    ],
)
class TestRepository:
    def test_init(self, klass: Callable[[AsyncSession], AbstractRepository]) -> None:
        session = Mock()
        repository = klass(session)
        assert repository.session is session

    async def test_create(self, klass: Callable[[AsyncSession], AbstractRepository]) -> None:
        session = Mock()
        repository = klass(session)
        await repository.create(a=1, b=2)
