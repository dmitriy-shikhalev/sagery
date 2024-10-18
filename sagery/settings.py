from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresqlSettings(BaseSettings):
    """Settings for PostgreSQL database connection."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="POSTGRESQL_", extra="allow")

    host: str
    port: int
    db_name: str
    user: str
    password: str


class CommonSettings(BaseSettings):
    """Common server settings."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="COMMON_", extra="allow")

    host: str = "localhost"
    port: int = 8000
    jobs_list_filename: str = "jobs_list.json"
    operators_list_filename: str = "operators_list.json"


class Settings(BaseSettings):
    """Hole settings class."""

    model_config = SettingsConfigDict(env_file=".env")

    sqlalchemy_url: AnyUrl
    postgresql: PostgresqlSettings = PostgresqlSettings()
    common: CommonSettings = CommonSettings()
