import logging


logging.basicConfig(level=logging.INFO)


def worker():
    raise NotImplementedError


def create_job():
    raise NotImplementedError


def get_status():
    raise NotImplementedError


def get_result():
    raise NotImplementedError


def main():
    raise NotImplementedError
