from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sagery.engine import get_async_engine
from sagery.job_starter import JobStarter
from sagery.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.settings = Settings()  # type: ignore
    engine = get_async_engine(app.state.settings.postgres)
    app.state.job_starter = JobStarter(engine, app.state.settings.job_starter)
    await app.state.job_starter.start()

    yield

    await app.state.job_starter.stop()
    await engine.dispose()


app = FastAPI(title="sagery", lifespan=lifespan)
