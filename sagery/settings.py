from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresqlSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='POSTGRESQL_', extra='allow')

    host: str
    port: int
    db_name: str
    user: str
    password: str


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='COMMON_', extra='allow')

    host: str = 'localhost'
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    sqlalchemy_url: AnyUrl
    postgresql: PostgresqlSettings = PostgresqlSettings()
    common: CommonSettings = CommonSettings()
