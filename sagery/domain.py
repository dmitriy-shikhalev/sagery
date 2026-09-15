from dataclasses import dataclass
from typing import TypeAlias

from sagery.enums import Status


# Block schema


type QueueName = str
type OperatorName = str


@dataclass
class Operator:
    name: str
    inputs: set[QueueName]
    outputs: set[QueueName]


@dataclass
class Saga:
    id: int
    name: str
    operators: dict[OperatorName, Operator]
    queues: set[QueueName]


# Block jobs


@dataclass
class Launch:
    id: int
    operator: OperatorName
    status: Status


@dataclass
class Value:
    data: Any
    done: bool


@dataclass
class Stream:
    name: QueueName
    values: list[Value]
    done: bool


@dataclass
class Job:
    saga_id: int
    streams: dict[QueueName, Stream]
    launches: dict[OperatorName, Launch]
    status: Status
