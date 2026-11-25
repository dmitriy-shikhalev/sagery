from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sagery.settings import Settings
from sagery.storage import Storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.settings = Settings()  # type: ignore
    app.state.sagas = app.state.settings.get_sagas_dict()
    app.state.storage = Storage(app.state.sagas)

    yield


app = FastAPI(title="sagery", lifespan=lifespan)
