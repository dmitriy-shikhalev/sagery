from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRESQL_DB_NAME: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
