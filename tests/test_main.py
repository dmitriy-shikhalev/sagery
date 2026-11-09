from unittest.mock import Mock, patch

from sagery.main import main


@patch("sagery.main.app")
@patch("sagery.main.Settings")
@patch("sagery.main.uvicorn.run")
def test_main(run_mock: Mock, settings_mock: Mock, app_mock: Mock) -> None:
    main()

    settings_mock.assert_called_once_with()
    run_mock.assert_called_once_with(
        app_mock, host=settings_mock.return_value.api.host, port=settings_mock.return_value.api.port
    )
