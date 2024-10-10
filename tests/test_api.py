from fastapi.testclient import TestClient

from sagery.main import app

client = TestClient(app)


def test_create_job(session):
    raise ZeroDivisionError(session)
