from __future__ import annotations

from sagery.operators import AbstractOperator


class Saga:
    def __init__(self, name: str, queues: set[str], operators: dict[str, Operator]):
        self.name = name
        self.queues = queues
        self.operators = operators


class Operator:
    def __init__(self, name: str, operator_cls: type[AbstractOperator]):
        self.name = name
        self.operator_cls = operator_cls
