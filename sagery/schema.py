from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from sagery.enums import JobStatus, OperatorStatus
from sagery.operators import AbstractOperator


class Saga:  # todo
    name: str
    queues: set[str]
    operators: dict[str, Operator]


class Operator:  # todo
    name: str
    object: AbstractOperator = Field(exclude=True)
    inputs: set[str]
    outputs: set[str]
