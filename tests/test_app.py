from unittest.mock import Mock, patch

from sagery import app


@patch("sagery.app.Storage")
@patch("sagery.app.Settings")
async def test_lifespan(settings_mock: Mock, storage_mock: Mock) -> None:
    app_mock = Mock()

    async with app.lifespan(app_mock):
        pass

    settings_mock.assert_called_once_with()
    assert app_mock.state.settings == settings_mock.return_value
    settings_mock.return_value.get_sagas_dict.assert_called_once_with()
    assert app_mock.state.sagas == settings_mock.return_value.get_sagas_dict.return_value
    storage_mock.assert_called_once_with(app_mock.state.sagas)
    assert app_mock.state.storage == storage_mock.return_value
