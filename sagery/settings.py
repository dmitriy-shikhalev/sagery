from importlib import import_module
from pathlib import Path
from typing import ClassVar, cast

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

from sagery.operators import AbstractOperator
from sagery.schema import Operator as SchemaOperator
from sagery.schema import Saga as SchemaSaga


class ApiSettings(BaseModel):
    host: str
    port: int


class Operator(BaseSettings):
    package: str
    module: str
    klass: str
    name: str

    def get_operator(self) -> type[AbstractOperator]:
        mod = import_module(f"{self.package}.{self.module}")
        klass = cast(type[AbstractOperator], getattr(mod, self.klass))
        if not issubclass(klass, AbstractOperator):
            raise ValueError(f"Object {self.package}.{self.module}.{self.klass} is not Operator")
        return klass

    def to_model(self) -> SchemaOperator:
        return SchemaOperator(
            name=self.name,
            operator_cls=self.get_operator(),
        )


class Saga(BaseSettings):
    name: str
    queues: list[str]
    operators: list[Operator]

    def to_model(self) -> SchemaSaga:
        return SchemaSaga(
            name=self.name,
            queues=set(self.queues),
            operators={operator.name: operator.to_model() for operator in self.operators},
        )


class Settings(BaseSettings):
    config_file: ClassVar[Path] = Path("config.yaml")

    sagas: list[Saga]
    api: ApiSettings

    def get_sagas_dict(self) -> dict[str, SchemaSaga]:
        return {s.name: s.to_model() for s in self.sagas}

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
