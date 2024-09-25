from unittest.mock import patch, Mock

from sagery.api import app
from sagery.enums import Mode
from sagery.main import main


@patch("sagery.main.Settings")
@patch("sagery.main.uvicorn.run")
@patch("sagery.main.argparse.ArgumentParser", return_value=Mock(
    parse_args=Mock(
        return_value=Mock(
            mode='web'
        )
    ),
))
def test_main_web(argument_parser_mock, run_mock, settings_mock):
    # pylint: disable=missing-function-docstring
    main()

    argument_parser_mock.assert_called_once()
    argument_parser_mock.return_value.add_argument.assert_called_once_with('mode', help='mode', choices=Mode)
    argument_parser_mock.return_value.parse_args.assert_called_once_with()

    run_mock.assert_called_once_with(
        app,
        host=settings_mock.return_value.common.host,
        port=settings_mock.return_value.common.port
    )


@patch("sagery.main.run")
@patch("sagery.main.argparse.ArgumentParser", return_value=Mock(
    parse_args=Mock(
        return_value=Mock(
            mode='core'
        )
    ),
))
def test_main_core(argument_parser_mock, run_mock):
    # pylint: disable=missing-function-docstring
    main()

    argument_parser_mock.assert_called_once()
    argument_parser_mock.return_value.add_argument.assert_called_once_with('mode', help='mode', choices=Mode)
    argument_parser_mock.return_value.parse_args.assert_called_once_with()

    run_mock.assert_called_once_with()
