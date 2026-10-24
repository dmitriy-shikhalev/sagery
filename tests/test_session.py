from pytest import fixture
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from sagery.session import get_engine, get_sessionmaker
from sagery.settings import Settings


@fixture(scope="session")
def engine(settings: Settings) -> Engine:
    return get_engine(settings.postgres)


@fixture(scope="session")
def sessionmaker_fxt(engine: Engine) -> sessionmaker[Session]:
    return get_sessionmaker(engine)


async def test_session(sessionmaker_fxt: sessionmaker[Session]) -> None:
    pass
