from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sagery.settings import PostgresqlSettings


def get_engine():
    settings = PostgresqlSettings()
    engine = create_engine(
        f"postgresql+psycopg2://{settings.user}:{settings.password}"
        f"@{settings.host}:{settings.port}/{settings.database}/"
    )
    return engine


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
