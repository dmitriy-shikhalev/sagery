from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from sagery.enums import JobStatus, OperatorStatus
from sagery.operators import AbstractOperator

# Schema


class Saga(BaseModel):
    name: str
    queues: set[str]
    operators: dict[str, Operator]


class Operator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    object: AbstractOperator = Field(exclude=True)
    inputs: set[str]
    outputs: set[str]


# Jobs


class Job(BaseModel):
    id: str
    saga_name: str
    status: JobStatus
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    comment: str = ""

    streams: dict[str, Stream] = Field(default_factory=dict)


class Stream(BaseModel):
    queue_name: str
    values: list[Any]


class Launch(BaseModel):
    id: str
    job_id: str
    operator_name: str
    # state: dict ???
    status: OperatorStatus
