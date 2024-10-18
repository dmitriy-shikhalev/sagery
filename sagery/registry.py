from importlib import import_module
from typing import Generic, TypeVar

from sagery.operators import AbstractOperator
from sagery.sagas import AbstractSaga

ElementClass = TypeVar("ElementClass")


class Registry(Generic[ElementClass]):
    """Common class for registers."""

    def __init__(self):  # noqa: D107
        self._registry: dict[str, ElementClass] = {}

    def register(self, klass: ElementClass):
        """Register a new class."""
        self._registry[klass.__name__] = klass  # type: ignore  # todo: find how to solve this error in mypy check

    def get(self, name: str) -> ElementClass | None:
        """Get a class by name."""
        return self._registry.get(name)


SAGA_REGISTRY = Registry[AbstractSaga]()
OPERATOR_REGISTRY = Registry[AbstractOperator]()


def import_class(filename, class_name):
    """Import class by filename and class_name."""
    module = import_module(filename, filename)
    return getattr(module, class_name)


def collect_all(sagas: list[str], operators: list[str]):
    """Collect all registered classes: jobs and operators."""
    sagas_python = [import_class(saga.split(":")[0], saga.split(":")[1]) for saga in sagas]
    for saga in sagas_python:
        SAGA_REGISTRY.register(saga)

    operators_python = [import_class(operator.split(":")[0], operator.split(":")[1]) for operator in operators]
    for operator in operators_python:
        OPERATOR_REGISTRY.register(operator)
