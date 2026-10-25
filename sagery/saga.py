from pydantic import BaseModel


class Operator(BaseModel):
    name: str
    inputs: list[str]
    outputs: list[str]


class Saga(BaseModel):
    name: str
    queues: list[str]
    operators: list[Operator]
