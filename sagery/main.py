import uvicorn

from sagery.api.app import app


def main() -> None:
    uvicorn.run(app, host="localhost", port=8000)
