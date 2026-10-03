from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    url: PostgresDsn


class ApiSettings(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8")

    api: ApiSettings
    postgres: PostgresSettings
