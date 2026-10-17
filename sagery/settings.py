from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    url: PostgresDsn


class ApiSettings(BaseModel):
    host: str
    port: int


class JobStarterSettings(BaseModel):
    max_count: int
    sleep_time: float


class Operator(BaseModel):
    name: str
    inputs: list[str]
    outputs: list[str]


class Saga(BaseModel):
    name: str
    queues: list[str]
    operators: list[Operator]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8")

    sagas: list[Saga]
    api: ApiSettings
    postgres: PostgresSettings
    job_starter: JobStarterSettings
