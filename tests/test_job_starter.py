from unittest.mock import Mock

import pytest

from sagery.job_starter import JobStarter


@pytest.fixture()
def engine() -> Mock:
    return Mock()


@pytest.fixture()
def settings() -> Mock:
    return Mock()


@pytest.fixture()
def job_starter(engine: Mock, settings: Mock) -> JobStarter:
    return JobStarter(engine, settings)


class TestJobStarter:
    def test_init(self, job_starter: Mock, engine: Mock, settings: Mock) -> None:
        assert job_starter.engine is engine
        assert job_starter.count == 0
        assert job_starter.max_count == settings.max_count
        assert job_starter.sleep_time == settings.sleep_time
        assert job_starter.job_coroutines == []

    async def test_start(self, job_starter: Mock) -> None:
        with pytest.raises(NotImplementedError):
            await job_starter.start()

    async def test_stop(self, job_starter: Mock) -> None:
        with pytest.raises(NotImplementedError):
            await job_starter.stop()
