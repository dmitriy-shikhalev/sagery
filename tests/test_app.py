from unittest.mock import Mock, patch

from sagery import app


@patch("sagery.app.Settings")
async def test_lifespan(settings_mock: Mock) -> None:
    app_mock = Mock()

    async with app.lifespan(app_mock):
        pass

    settings_mock.assert_called_once_with()
    assert app_mock.state.settings == settings_mock.return_value
