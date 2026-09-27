from collections.abc import Callable
from unittest.mock import AsyncMock, Mock, patch

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
        with patch.object(repository.converter, "from_domain_to_model") as from_domain_to_model_mock:
            result = await repository.create(object_)

            from_domain_to_model_mock.assert_called_once_with(object_)
            session.add.assert_called_once_with(from_domain_to_model_mock.return_value)
            session.flush.assert_called_once_with()
            assert object_.id == from_domain_to_model_mock.return_value.id
            assert result is object_

    @patch("sagery.repositories.select")
    async def test_get_none(
        self, select_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: domain_model
    ) -> None:
        id_ = 123
        session = Mock(execute=AsyncMock(return_value=Mock(first=Mock(return_value=None))))
        repository = klass(session)
        with patch.object(repository.converter, "from_model_to_domain") as from_model_to_domain_mock:
            result = await repository.get(id_)
            assert result is None

            select_mock.assert_called_once_with(repository.model)
            select_mock.return_value.where.assert_called_once()
            select_mock.return_value.where.return_value.limit.assert_called_once_with(1)

            session.execute.assert_called_once_with(select_mock.return_value.where.return_value.limit.return_value)
            session.execute.return_value.first.assert_called_once_with()

            from_model_to_domain_mock.assert_not_called()

    @patch("sagery.repositories.select")
    async def test_get_not_none(
        self, select_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: domain_model
    ) -> None:
        id_ = 123
        db_model_obj = Mock()
        session = Mock(execute=AsyncMock(return_value=Mock(first=Mock(return_value=db_model_obj))))
        repository = klass(session)
        with patch.object(repository.converter, "from_model_to_domain") as from_model_to_domain_mock:
            result = await repository.get(id_)
            assert result == from_model_to_domain_mock.return_value

            select_mock.assert_called_once_with(repository.model)
            select_mock.return_value.where.assert_called_once()
            select_mock.return_value.where.return_value.limit.assert_called_once_with(1)

            session.execute.assert_called_once_with(select_mock.return_value.where.return_value.limit.return_value)
            session.execute.return_value.first.assert_called_once_with()

            from_model_to_domain_mock.assert_called_once_with(db_model_obj)
