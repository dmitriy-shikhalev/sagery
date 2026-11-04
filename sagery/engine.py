from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from sagery.settings import PostgresSettings


def get_async_engine(settings: PostgresSettings) -> AsyncEngine:
    """
    Using this engine:
    meta = MetaData()
    t1 = Table("t1", meta, Column("name", String(50), primary_key=True))

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)
        await conn.execute(
            t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
        )
    """
    engine = create_async_engine(settings.url.unicode_string())
    return engine
