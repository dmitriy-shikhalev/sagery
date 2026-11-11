from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)


class PostgresSettings(BaseModel):
    url: PostgresDsn


class ApiSettings(BaseModel):
    host: str
    port: int


class JobStarterSettings(BaseModel):
    max_count: int
    sleep_time: float


class Operator(BaseSettings):
    name: str
    inputs: list[str]
    outputs: list[str]
    params: dict[str, Any] = Field(default_factory=dict)


class Saga(BaseSettings):
    name: str
    queues: list[str]
    operators: dict[str, Operator]


class Settings(BaseSettings):
    config_file: ClassVar[Path] = Path("config.yaml")

    sagas: dict[str, Saga]
    api: ApiSettings
    postgres: PostgresSettings
    job_starter: JobStarterSettings

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
