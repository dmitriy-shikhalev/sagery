from dataclasses import dataclass

from sagery.enums import Status


# Block schema


@dataclass
class Input:
    name: str


@dataclass
class Output:
    name: str


@dataclass
class Operator:
    name: str
    inputs: list[Input]
    outputs: list[Output]


@dataclass
class Queue:
    name: str


@dataclass
class Saga:
    id: int
    name: str
    operators: list[Operator]
    queues: list[Queue]


# Block jobs


@dataclass
class Launch:
    id: int
    operator: str
    status: Status


@dataclass
class Value:
    data: Any
    done: bool


@dataclass
class Stream:
    name: str
    values: list[Value]
    done: bool


@dataclass
class Job:
    saga_id: int
    streams: list[Stream]
    launches: list[Launch]
    status: Status
