import logging

import uvicorn

from sagery.api.v1 import app

logging.basicConfig(level=logging.INFO)


def worker():
    raise NotImplementedError
