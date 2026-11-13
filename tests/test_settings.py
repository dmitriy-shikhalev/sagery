from unittest.mock import Mock, patch

from sagery import settings


@patch("sagery.settings.YamlConfigSettingsSource")
def test_settings_customise_sources(source_mock: Mock) -> None:
    settings_cls = Mock()
    init_settings = Mock()
    env_settings = Mock()
    dotenv_settings = Mock()
    file_secret_settings = Mock()

    with patch.object(settings.Settings, "config_file") as config_file:
        s = settings.Settings.settings_customise_sources(
            settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings
        )

        source_mock.assert_called_once_with(settings_cls, yaml_file=config_file)
        assert s == (init_settings, source_mock.return_value)
