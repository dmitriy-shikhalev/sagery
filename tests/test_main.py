from unittest.mock import patch

from sagery.api.v1 import app
from sagery.main import web


@patch("sagery.main.uvicorn")
def test_web(uvicorn_mock):
    result = web()

    assert result is None

    uvicorn_mock.run.assert_called_once_with(app, host='0.0.0.0', port=8000)
