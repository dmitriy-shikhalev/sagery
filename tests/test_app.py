from unittest.mock import AsyncMock, Mock, patch

from sagery import app


@patch("sagery.app.get_async_engine", return_value=Mock(dispose=AsyncMock()))
@patch("sagery.app.Settings")
async def test_lifespan(settings_mock: Mock, get_async_engine_mock: Mock) -> None:
    app_mock = Mock()

    async with app.lifespan(app_mock):
        pass

    settings_mock.assert_called_once_with()
    assert app_mock.state.settings == settings_mock.return_value

    get_async_engine_mock.assert_called_once_with(app_mock.state.settings.postgres)

    get_async_engine_mock.return_value.dispose.assert_called_once_with()
