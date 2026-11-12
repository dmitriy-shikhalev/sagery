from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from sagery.main import get_args, main


@patch("sagery.main.argparse.ArgumentParser")
def test_get_args_ok(argument_parser_mock: Mock) -> None:
    result = get_args()

    argument_parser_mock.assert_called_once_with()
    argument_parser_mock.return_value.add_argument.assert_called_once_with(
        "-c", "--config", type=Path, required=False, default="config.yaml"
    )
    argument_parser_mock.return_value.parse_args.assert_called_once_with()
    assert result is argument_parser_mock.return_value.parse_args.return_value


def test_get_args_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    config = tmp_path / "config.yaml"
    monkeypatch.setattr("sys.argv", ["sagery", "-c", str(config)])

    with pytest.raises(SystemExit) as exc:
        get_args()

    assert exc.value.code == 2
    assert f"config not found: {config}" in capsys.readouterr().err


@patch("sagery.main.get_args")
@patch("sagery.main.app")
@patch("sagery.main.Settings")
@patch("sagery.main.uvicorn.run")
def test_main(run_mock: Mock, settings_mock: Mock, app_mock: Mock, get_args: Mock) -> None:
    main()

    get_args.assert_called_once_with()
    assert settings_mock.config_file == get_args.return_value.config
    settings_mock.assert_called_once_with()
    run_mock.assert_called_once_with(
        app_mock, host=settings_mock.return_value.api.host, port=settings_mock.return_value.api.port
    )
