from collections.abc import Generator
from unittest.mock import Mock

import pytest

from sagery.services import JobService, StreamService


@pytest.fixture()
def job_repository() -> Generator[Mock]:
    yield Mock()


@pytest.fixture()
def stream_repository() -> Generator[Mock]:
    yield Mock()


@pytest.fixture()
def value_repository() -> Generator[Mock]:
    yield Mock()


@pytest.fixture()
def launch_repository() -> Generator[Mock]:
    yield Mock()


@pytest.mark.parametrize(
    "klass",
    (JobService, StreamService),
)
def test_init(
    klass: Mock, job_repository: Mock, stream_repository: Mock, value_repository: Mock, launch_repository: Mock
) -> None:
    service = klass(
        job_repository=job_repository,
        stream_repository=stream_repository,
        value_repository=value_repository,
        launch_repository=launch_repository,
    )

    assert service.job_repository == job_repository
    assert service.stream_repository == stream_repository
    assert service.value_repository == value_repository
    assert service.launch_repository == launch_repository


@pytest.fixture()
def job_service(
    job_repository: Mock, stream_repository: Mock, value_repository: Mock, launch_repository: Mock
) -> Generator[JobService]:
    yield JobService(job_repository, stream_repository, value_repository, launch_repository)


@pytest.fixture()
def stream_service(
    job_repository: Mock, stream_repository: Mock, value_repository: Mock, launch_repository: Mock
) -> Generator[StreamService]:
    yield StreamService(job_repository, stream_repository, value_repository, launch_repository)


class TestJobService:
    async def test_run(self, job_service: Mock) -> None:
        id_ = Mock()
        with pytest.raises(NotImplementedError):
            await job_service.run(id_)


class TestStreamService:
    async def test_run(self, stream_service: Mock) -> None:
        id_ = Mock()
        with pytest.raises(NotImplementedError):
            await stream_service.run(id_)
