from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sagery.settings import PostgresqlSettings


def get_engine():
    """
    Return a sqlalchemy engine instance.
    """
    settings = PostgresqlSettings()
    engine = create_engine(
        f"postgresql+psycopg2://{settings.user}:{settings.password}"
        f"@{settings.host}:{settings.port}/{settings.db_name}"
    )
    return engine


@contextmanager
def get_session():
    """
    Return a sqlalchemy session instance.
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session
