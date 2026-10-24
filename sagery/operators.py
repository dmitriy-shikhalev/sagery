from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any


class AbstractOperator(ABC):
    @abstractmethod
    async def run(self) -> AsyncGenerator[tuple[str, Any] | None, tuple[str, Any]]:  # pragma: no coverage
        while False:
            yield  # Эта строка только для того, чтобы python понял, что .run - это асинхронный генератор
        raise NotImplementedError


class sum_2(AbstractOperator):
    async def run(self) -> AsyncGenerator[tuple[str, Any] | None, tuple[str, Any]]:
        print("start")
        var_name1, value1 = yield None
        if var_name1 != "a":
            raise NameError(f"Unknown variable {var_name1}")
        var_name2, value2 = yield None
        if var_name2 != "b":
            raise NameError(f"Unknown variable {var_name1}")

        yield "c", value1 + value2
