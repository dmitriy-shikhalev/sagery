from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from sagery.settings import PostgresSettings


def get_engine(settings: PostgresSettings) -> Engine:
    engine = create_engine(f"{settings.url.unicode_string()}")
    return engine


def get_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    Session = sessionmaker(engine)
    return Session
