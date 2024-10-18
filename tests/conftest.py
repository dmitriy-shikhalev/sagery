from typing import AsyncGenerator, Generator
from unittest.mock import Mock

from pytest import fixture
from sqlalchemy.orm import Session

from sagery.db import get_session
from sagery.main import app
from sagery.models import Job
from sagery.registry import collect_all
from sagery.repositories import JobRepository


@fixture()
def test_session() -> Generator[Session, None, None]:
    """Test session fixture"""  # noqa: D400, D415
    session = next(get_session(), None)
    if session is None:
        raise RuntimeError("Session is None!")

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@fixture()
def session_override():
    """Override the DB session."""
    session_mock = Mock()

    def get_session_override():
        return session_mock

    app.dependency_overrides[get_session] = get_session_override
    try:
        yield session_mock
    finally:
        app.dependency_overrides.clear()


@fixture()
async def job(test_session: Session) -> AsyncGenerator[Job, None]:
    """Job fixture."""
    job_ = await JobRepository(test_session).create(a="b")
    yield job_


@fixture()
async def example() -> None:
    """Example job and operator fixture."""  # noqa: D401
    collect_all(["tests.example.sagas:ExampleSaga"], ["tests.example.operators:ExampleOperator"])
