from typing import Any

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8")

    sagas: dict[str, Saga]
    api: ApiSettings
    postgres: PostgresSettings
    job_starter: JobStarterSettings
