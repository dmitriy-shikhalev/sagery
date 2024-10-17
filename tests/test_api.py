from fastapi import status
from fastapi.testclient import TestClient

from sagery.main import app

client = TestClient(app)


def test_create_job_not_found():
    """Test creating a job by POST /sagas/<job_name>/ with result "not found"."""
    test_job_name = "not_existed_saga_name"
    response = client.post(f"/sagas/{test_job_name}/", json={"name": test_job_name})

    assert response.status_code == status.HTTP_404_NOT_FOUND
