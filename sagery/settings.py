from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)


class RabbitMQSettings:
    host: str
    port: str
    login: str
    password: str


class QueueSettings(BaseModel):
    rabbitmq: RabbitMQSettings


class ApiSettings(BaseModel):
    host: str
    port: int


class Operator(BaseSettings):
    package: str
    module: str
    klass: str
    name: str
    inputs: list[str]
    outputs: list[str]
    params: dict[str, Any]


class Saga(BaseSettings):
    name: str
    queues: list[str]
    operators: list[Operator]


class Settings(BaseSettings):
    config_file: ClassVar[Path] = Path("config.yaml")

    sagas: list[Saga]
    api: ApiSettings
    postgres: PostgresSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,  # намеренно не используется
        dotenv_settings: PydanticBaseSettingsSource,  # намеренно не используется
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls, yaml_file=cls.config_file),
        )
