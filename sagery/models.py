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
