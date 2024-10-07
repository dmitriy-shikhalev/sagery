import argparse
import logging

import uvicorn

from sagery.api import app
from sagery.daemon import run
from sagery.enums import Mode
from sagery.settings import Settings

logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function. Entry point for web and core.
    """
    args = argparse.ArgumentParser()
    args.add_argument("mode", help="mode", choices=Mode)

    settings = Settings()
    match args.parse_args().mode:
        case Mode.WEB:
            uvicorn.run(app, host=settings.common.host, port=settings.common.port)
        case Mode.CORE:
            run()
