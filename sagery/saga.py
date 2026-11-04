from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class Operator(BaseSettings):
    name: str
    inputs: list[str]
    outputs: list[str]
    params: dict[str, Any] = Field(default_factory=dict)


class Saga(BaseSettings):
    name: str
    queues: list[str]
    operators: list[Operator]
