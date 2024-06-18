from fastapi import FastAPI

from sagery.api import main


def test_app_exists():
    assert isinstance(main.app, FastAPI)
