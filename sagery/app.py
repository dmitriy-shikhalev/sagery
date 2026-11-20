from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sagery.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.settings = Settings()  # type: ignore
    app.state.sagas = app.state.settings.get_sagas_dict()

    yield


app = FastAPI(title="sagery", lifespan=lifespan)
