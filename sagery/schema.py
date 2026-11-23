from __future__ import annotations

from sagery.operators import AbstractOperator


class Saga:
    def __init__(self, name: str, queues: set[str], operators: dict[str, Operator]):
        self.name = name
        self.queues = queues
        self.operators = operators


class Operator:
    def __init__(self, name: str, object: AbstractOperator, inputs: set[str], outputs: set[str]):
        self.name = name
        self.object = object
        self.inputs = inputs
        self.outputs = outputs
