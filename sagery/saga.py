from pydantic_settings import BaseSettings


class Operator(BaseSettings):
    name: str
    inputs: list[str]
    outputs: list[str]


class Saga(BaseSettings):
    name: str
    queues: list[str]
    operators: list[Operator]
