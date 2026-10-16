from unittest.mock import AsyncMock, Mock, patch

from sagery.api import app


@patch("sagery.api.app.JobStarter", return_value=Mock(start=AsyncMock(), stop=AsyncMock()))
@patch("sagery.api.app.get_async_engine", return_value=Mock(dispose=AsyncMock()))
@patch("sagery.api.app.Settings")
async def test_lifespan(settings_mock: Mock, get_async_engine_mock: Mock, job_starter_mock: Mock) -> None:
    app_mock = Mock()

    async with app.lifespan(app_mock):
        pass

    settings_mock.assert_called_once_with()
    assert app_mock.state.settings == settings_mock.return_value

    get_async_engine_mock.assert_called_once_with(app_mock.state.settings.postgres)
    job_starter_mock.assert_called_once_with(get_async_engine_mock.return_value, app_mock.state.settings.job_starter)
    assert app_mock.state.job_starter == job_starter_mock.return_value
    job_starter_mock.return_value.start.assert_called_once_with()

    job_starter_mock.return_value.stop.assert_called_once_with()
    get_async_engine_mock.return_value.dispose.assert_called_once_with()
