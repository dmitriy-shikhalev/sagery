from importlib import import_module
from pathlib import Path
from typing import Any, ClassVar, cast

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

from sagery.enums import QueueEngine
from sagery.operators import AbstractOperator
from sagery.schema import Operator as ModelOperator
from sagery.schema import Saga as ModelSaga


class LocalQueueSettings(BaseSettings):
    pass


class RabbitMQSettings(BaseSettings):
    host: str
    port: str
    login: str
    password: str


class QueueSettings(BaseModel):
    engine: QueueEngine
    local_queue: LocalQueueSettings | None = None
    rabbitmq: RabbitMQSettings | None = None


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

    def get_operator(self) -> AbstractOperator:
        mod = import_module(f"{self.package}.{self.module}")
        klass = cast(type[AbstractOperator], getattr(mod, self.klass))
        if not issubclass(klass, AbstractOperator):
            raise ValueError(f"Object {self.package}.{self.module}.{self.klass} is not Operator")
        return klass(**self.params)

    def to_model(self) -> ModelOperator:
        return ModelOperator(
            name=self.name,
            object=self.get_operator(),
            inputs=set(self.inputs),
            outputs=set(self.outputs),
        )


class Saga(BaseSettings):
    name: str
    queues: list[str]
    operators: list[Operator]

    def to_model(self) -> ModelSaga:
        return ModelSaga(
            name=self.name,
            queues=set(self.queues),
            operators={operator.name: operator.to_model() for operator in self.operators},
        )


class Settings(BaseSettings):
    config_file: ClassVar[Path] = Path("config.yaml")

    sagas: list[Saga]
    api: ApiSettings
    queue: QueueSettings

    def get_sagas_dict(self) -> dict[str, ModelSaga]:
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
