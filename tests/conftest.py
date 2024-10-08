from sqlalchemy.orm import Session

from pytest import fixture

from sagery.db import get_session


@fixture()
def session() -> Session:
    with get_session() as session:
        try:
            yield session
        finally:
            session.rollback()
            session.close()
