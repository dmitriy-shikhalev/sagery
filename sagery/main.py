import uvicorn

from sagery.api.app import app
from sagery.settings import Settings


def main() -> None:
    settings = Settings()  # type: ignore
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
