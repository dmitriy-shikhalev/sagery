from collections.abc import Callable
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sagery import domain
from sagery.repositories import AbstractRepository, SagaRepository
from sagery.types import DBModel, DomainModel


@pytest.mark.parametrize(
    ["klass", "object_"],
    [
        (SagaRepository, domain.Saga(id=10**5, name="abc", comment="comment", operators={}, queues={})),
    ],
)
class TestRepository[db_model_type: DBModel, domain_model: DomainModel]:
    def test_init(self, klass: Callable[[AsyncSession], AbstractRepository], object_: domain_model) -> None:
        session = Mock()
        repository = klass(session)
        assert repository.session is session

    async def test_create(self, klass: Callable[[AsyncSession], AbstractRepository], object_: domain_model) -> None:
        session = AsyncMock()
        repository = klass(session)
        await repository.create(object_)
