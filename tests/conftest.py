from typing import AsyncGenerator, Generator

from pytest import fixture
from sqlalchemy.orm import Session

from sagery.db import get_session
from sagery.models import Job
from sagery.repositories import JobRepository


@fixture()
def test_session() -> Generator[Session, None, None]:
    # pylint: disable=missing-function-docstring, not-context-manager
    with get_session() as session:
        try:
            yield session
        finally:
            session.rollback()
            session.close()


@fixture()
async def job(test_session: Session) -> AsyncGenerator[Job, None]:  # pylint: disable=redefined-outer-name
    """
    Job fixture.
    """
    job_ = await JobRepository(test_session).create(a='b')
    yield job_
