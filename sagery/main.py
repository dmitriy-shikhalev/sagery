import argparse
import logging

import uvicorn

from sagery.api import app
from sagery.core import run
from sagery.enums import Mode
from sagery.settings import Settings


logging.basicConfig(level=logging.INFO)


def main():
    settings = Settings()

    args = argparse.ArgumentParser()
    args.add_argument("mode", help="mode", choices=Mode)

    match args.parse_args().mode:
        case Mode.WEB:
            uvicorn.run(app, host=settings.common.host, port=settings.common.port)
        case Mode.CORE:
            run()
