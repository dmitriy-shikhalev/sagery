from typing import Generator

from pytest import fixture
from sqlalchemy.orm import Session

from sagery.db import get_session


@fixture()
def session() -> Generator[Session, None, None]:
    # pylint: disable=missing-function-docstring, not-context-manager
    with get_session() as _session:
        try:
            yield _session
        finally:
            _session.rollback()
            _session.close()
