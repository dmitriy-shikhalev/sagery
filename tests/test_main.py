from unittest.mock import Mock, patch

from sagery.api import app
from sagery.enums import Mode
from sagery.main import main


@patch("sagery.main.collect_all")
@patch("sagery.main.read_list_from_json_file")
@patch("sagery.main.Settings")
@patch("sagery.main.uvicorn.run")
@patch(
    "sagery.main.argparse.ArgumentParser",
    return_value=Mock(
        parse_args=Mock(return_value=Mock(mode='web')),
    ),
)
def test_main_web(  # noqa: D103
    argument_parser_mock, run_mock, settings_mock, read_list_from_json_file_mock, collect_all_mock
):
    main()

    argument_parser_mock.assert_called_once()
    argument_parser_mock.return_value.add_argument.assert_called_once_with('mode', help='mode', choices=Mode)
    argument_parser_mock.return_value.parse_args.assert_called_once_with()

    settings_mock.assert_called_once_with()

    run_mock.assert_called_once_with(
        app, host=settings_mock.return_value.common.host, port=settings_mock.return_value.common.port
    )

    read_list_from_json_file_mock.assert_any_call(settings_mock.return_value.common.jobs_list_filename)
    read_list_from_json_file_mock.assert_any_call(settings_mock.return_value.common.operators_list_filename)

    collect_all_mock.assert_called_once_with(
        read_list_from_json_file_mock.return_value,
        read_list_from_json_file_mock.return_value,
    )


@patch("sagery.main.collect_all")
@patch("sagery.main.read_list_from_json_file")
@patch("sagery.main.Settings")
@patch("sagery.main.run")
@patch(
    "sagery.main.argparse.ArgumentParser",
    return_value=Mock(
        parse_args=Mock(return_value=Mock(mode='core')),
    ),
)
def test_main_core(  # noqa: D103
    argument_parser_mock, run_mock, settings_mock, read_list_from_json_file_mock, collect_all_mock
):
    main()

    argument_parser_mock.assert_called_once()
    argument_parser_mock.return_value.add_argument.assert_called_once_with('mode', help='mode', choices=Mode)
    argument_parser_mock.return_value.parse_args.assert_called_once_with()

    run_mock.assert_called_once_with()

    settings_mock.assert_called_once_with()

    read_list_from_json_file_mock.assert_any_call(settings_mock.return_value.common.jobs_list_filename)
    read_list_from_json_file_mock.assert_any_call(settings_mock.return_value.common.jobs_list_filename)

    collect_all_mock.assert_called_once_with(
        read_list_from_json_file_mock.return_value,
        read_list_from_json_file_mock.return_value,
    )
