from dataclasses import dataclass, field
from typing import Any

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
    id: int
    saga_name: str
    streams: dict[QueueName, Stream]
    launches: dict[OperatorName, Launch]
    status: Status


@dataclass
class App:
    sagas: dict[str, Saga] = field(default_factory=dict)
    jobs: dict[int, Job] = field(default_factory=dict)
