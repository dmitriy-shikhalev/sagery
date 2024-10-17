import argparse
import json
import logging

import uvicorn

from sagery.api import app
from sagery.daemon import run
from sagery.enums import Mode
from sagery.registry import collect_all
from sagery.settings import Settings

logging.basicConfig(level=logging.INFO)


def read_list_from_json_file(filename):
    """Reads a JSON file and returns a list of content."""  # noqa: D401
    return json.load(
        open(
            filename,
            encoding='utf-8',
        )
    )


def main():
    """Main function. Entry point for web and core."""  # noqa: D401
    args = argparse.ArgumentParser()
    args.add_argument("mode", help="mode", choices=Mode)

    settings = Settings()

    jobs = read_list_from_json_file(settings.common.jobs_list_filename)
    operators = read_list_from_json_file(settings.common.operators_list_filename)

    collect_all(jobs, operators)

    match args.parse_args().mode:
        case Mode.WEB:
            uvicorn.run(app, host=settings.common.host, port=settings.common.port)
        case Mode.CORE:
            run()
