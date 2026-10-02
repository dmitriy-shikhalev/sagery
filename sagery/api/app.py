from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Здесь должен создаваться JobsStarter (или Runner) и OperatorStarter/Runner (?) и что еще?
    # Все это положить в app.state
    raise NotImplementedError
    # Здесь должны гаситься все запущенные треды
    yield


app = FastAPI(title="sagery", lifespan=lifespan)
