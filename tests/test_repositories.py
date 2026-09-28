from collections.abc import Callable
from unittest.mock import AsyncMock, Mock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sagery.repositories import (
    AbstractRepository,
    InputRepository,
    JobRepository,
    LaunchRepository,
    OperatorRepository,
    OutputRepository,
    QueueRepository,
    SagaRepository,
    StreamRepository,
    ValueRepository,
)
from sagery.types import DBModel


@pytest.mark.parametrize(
    ["klass", "object_"],
    [
        (SagaRepository, {"id": 10**5, "name": "abc", "comment": "comment"}),
        (QueueRepository, {"id": 10**5, "saga_id": 1, "name": "some-name"}),
        (OperatorRepository, {"id": 10**5, "saga_id": 1, "name": "some-name"}),
        (InputRepository, {"id": 10**5, "operator_id": 1, "queue_id": 1}),
        (OutputRepository, {"id": 10**5, "operator_id": 1, "queue_id": 1}),
        (JobRepository, {"id": 10**5, "saga_id": 1, "comment": "comment", "status": "done"}),
        (StreamRepository, {"id": 10**5, "job_id": 1, "queue_id": 1, "done": False}),
        (ValueRepository, {"id": 10**5, "stream_id": 1, "launch_id": 1, "data": {"a": "b"}, "done": True}),
        (LaunchRepository, {"id": 10**5, "job_id": 1, "operator_id": 1, "status": "done"}),
    ],
)
class TestRepository[db_model_type: DBModel]:
    def test_init(self, klass: Callable[[AsyncSession], AbstractRepository], object_: dict) -> None:
        session = Mock()
        repository = klass(session)
        assert repository.session is session

    async def test_create(self, klass: Callable[[AsyncSession], AbstractRepository], object_: dict) -> None:
        session = AsyncMock()
        repository = klass(session)

        result = await repository.create(object_)

        session.flush.assert_called_once_with()
        assert isinstance(result, repository.model)
        for k, v in object_.items():
            assert getattr(result, k) == v

    @patch("sagery.repositories.select")
    async def test_get_none(
        self, select_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: dict
    ) -> None:
        id_ = 123
        session = Mock(execute=AsyncMock(return_value=Mock(first=Mock(return_value=None))))
        repository = klass(session)

        result = await repository.get(id_)
        assert result is None

        select_mock.assert_called_once_with(repository.model)
        select_mock.return_value.where.assert_called_once()
        select_mock.return_value.where.return_value.limit.assert_called_once_with(1)

        session.execute.assert_called_once_with(select_mock.return_value.where.return_value.limit.return_value)
        session.execute.return_value.first.assert_called_once_with()

    @patch("sagery.repositories.select")
    async def test_get_not_none(
        self, select_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: dict
    ) -> None:
        id_ = 123
        db_model_obj = Mock()
        session = Mock(execute=AsyncMock(return_value=Mock(first=Mock(return_value=db_model_obj))))
        repository = klass(session)

        result = await repository.get(id_)
        assert result == db_model_obj

        select_mock.assert_called_once_with(repository.model)
        select_mock.return_value.where.assert_called_once()
        select_mock.return_value.where.return_value.limit.assert_called_once_with(1)

        session.execute.assert_called_once_with(select_mock.return_value.where.return_value.limit.return_value)
        session.execute.return_value.first.assert_called_once_with()

    @patch("sagery.repositories.select")
    async def test_filter_with_limit_with_offset(
        self, select_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: dict
    ) -> None:
        db_model_obj = Mock()
        session = Mock(execute=AsyncMock(return_value=Mock(all=Mock(return_value=[db_model_obj]))))
        repository = klass(session)

        result = await repository.filter({"a": "b", "c": "d"}, limit=10, offset=20)
        assert result == [db_model_obj]

        select_mock.assert_called_once_with(repository.model)
        select_mock.return_value.filter_by.assert_called_once_with(a="b", c="d")
        select_mock.return_value.filter_by.return_value.limit.assert_called_once_with(10)
        select_mock.return_value.filter_by.return_value.limit.return_value.offset.assert_called_once_with(20)

        session.execute.assert_called_once_with(
            select_mock.return_value.filter_by.return_value.limit.return_value.offset.return_value
        )
        session.execute.return_value.all.assert_called_once_with()

    @patch("sagery.repositories.update")
    async def test_update(
        self, update_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: dict
    ) -> None:
        session = AsyncMock()
        repository = klass(session)

        result = await repository.update({"a": "b", "c": "d"}, {"e": "f"})

        update_mock.assert_called_once_with(repository.model)
        update_mock.return_value.filter_by.assert_called_once_with(a="b", c="d")
        update_mock.return_value.filter_by.return_value.values.assert_called_once_with(e="f")
        session.execute.assert_called_once_with(update_mock.return_value.filter_by.return_value.values.return_value)
        assert result == session.execute.return_value.rowcount

    @patch("sagery.repositories.delete")
    async def test_delete(
        self, delete_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: dict
    ) -> None:
        session = AsyncMock()
        repository = klass(session)

        result = await repository.delete({"a": "b", "c": "d"})

        delete_mock.assert_called_once_with(repository.model)
        delete_mock.return_value.filter_by.assert_called_once_with(a="b", c="d")
        session.execute.assert_called_once_with(delete_mock.return_value.filter_by.return_value)
        assert result == session.execute.return_value.rowcount

    @patch("sagery.repositories.delete")
    async def test_delete_empty_filer(
        self, delete_mock: Mock, klass: Callable[[AsyncSession], AbstractRepository], object_: dict
    ) -> None:
        session = AsyncMock()
        repository = klass(session)

        with pytest.raises(ValueError):
            await repository.delete({})

        delete_mock.assert_not_called()
        session.execute.assert_not_called()
