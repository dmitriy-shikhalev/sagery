from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sagery.engine import get_async_engine
from sagery.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Здесь должен создаваться JobsStarter (или Runner) и OperatorStarter/Runner (?) и что еще?
    # Все это положить в app.state
    app.state.settings = Settings()  # type: ignore
    app.state.job_starter = JobStarter()
    app.state.job_starter.engine = get_async_engine(app.state.settings.postgres)
    yield
    # Здесь должны гаситься все запущенные треды


app = FastAPI(title="sagery", lifespan=lifespan)
