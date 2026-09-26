from dataclasses import dataclass, field
from typing import Any

from sagery.enums import Status

# Block types


type IDType = int
type IDTypeOrNone = IDType | None
type QueueName = str
type OperatorName = str


# Block schema


@dataclass
class Input:
    id: IDTypeOrNone
    operator_id: IDType
    queue_id: IDType


@dataclass
class Output:
    id: IDTypeOrNone
    operator_id: IDType
    queue_id: IDType


@dataclass
class Queue:
    id: IDTypeOrNone
    name: QueueName


@dataclass
class Operator:
    id: IDTypeOrNone
    name: str
    inputs: list[Input]
    outputs: list[Output]


@dataclass
class Saga:
    id: IDTypeOrNone
    name: str
    comment: str | None
    operators: dict[OperatorName, Operator]
    queues: dict[QueueName, Queue]


# Block jobs


@dataclass
class Launch:
    id: IDTypeOrNone
    operator: OperatorName
    status: Status


@dataclass
class Value:
    id: IDTypeOrNone
    data: Any
    done: bool


@dataclass
class Stream:
    id: IDTypeOrNone
    name: QueueName
    values: list[Value]
    done: bool


@dataclass
class Job:
    id: IDTypeOrNone
    saga_name: str
    streams: dict[QueueName, Stream]
    launches: dict[OperatorName, Launch]
    status: Status


@dataclass
class App:
    sagas: dict[str, Saga] = field(default_factory=dict)
    jobs: dict[int, Job] = field(default_factory=dict)
