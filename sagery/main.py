import logging

import uvicorn

from sagery.api.v1 import app

logging.basicConfig(level=logging.INFO)


def web():
    uvicorn.run(app, host='0.0.0.0', port=8000)


def worker():
    raise NotImplementedError
