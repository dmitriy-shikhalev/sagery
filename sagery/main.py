import argparse
from pathlib import Path

import uvicorn

from sagery.app import app
from sagery.settings import Settings


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, required=False, default="config.yaml")
    args = parser.parse_args()

    if not args.config.is_file():
        parser.error(f"config not found: {args.config}")

    return args


def main() -> None:
    args = get_args()
    Settings.config_file = args.config

    settings = Settings()  # type: ignore
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
