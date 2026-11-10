# Загрузка настроек из YAML в pydantic-settings с путём из аргумента

Используй встроенный `YamlConfigSettingsSource` и передавай путь через `argparse`. Источник читает `yaml_file` при создании `Settings()`, поэтому путь надо выставить до инстанцирования.

```python
# sagery/settings.py
from pathlib import Path
from typing import ClassVar

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
    )

    config_file: ClassVar[Path] = Path("config.yaml")

    sagas: list[Saga]
    api: ApiSettings
    postgres: PostgresSettings
    job_starter: JobStarterSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls, yaml_file=cls.config_file),
        )
```

```python
# sagery/main.py
import argparse
from pathlib import Path

from sagery.settings import Settings

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=Path, required=True)
args = parser.parse_args()

if not args.config.is_file():
    parser.error(f"config not found: {args.config}")

Settings.config_file = args.config
settings = Settings()
```

Важно:

- Нужен `PyYAML`: `poetry add "pydantic-settings[yaml]"` или `poetry add pyyaml`.
- Порядок в `settings_customise_sources` — это приоритет: сейчас env/`.env` перекрывают YAML. Если YAML должен быть главнее env — поставь `YamlConfigSettingsSource` раньше.
- Несуществующий YAML-файл источник молча игнорирует, поэтому проверка `is_file()` выше желательна.
- Если YAML обёрнут в секцию, например `sagery:`, передай `yaml_config_section="sagery"`.
- Альтернатива без `ClassVar`: `Settings.model_config["yaml_file"] = args.config` перед `Settings()` (при условии, что в `settings_customise_sources` вызывается `YamlConfigSettingsSource(settings_cls)` без явного пути).
