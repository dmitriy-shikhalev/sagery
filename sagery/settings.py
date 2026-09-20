from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    url: PostgresDsn


class Settings(BaseSettings):
    postgres: PostgresSettings
