import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from sagery.enums import OperatorStatus

logger = logging.getLogger(__name__)


class AbstractOperator(ABC):
    task: asyncio.Task | None = None

    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs
        self.inputs: asyncio.Queue[tuple[str, Any]] = asyncio.Queue()
        self.outputs: asyncio.Queue[tuple[str, Any]] = asyncio.Queue()

    @property
    def status(self) -> OperatorStatus:
        if self.task is None:
            return OperatorStatus.NOT_STARTED
        elif self.task.done():
            if self.task.cancelled():
                return OperatorStatus.ABORTED
            elif self.task.exception():
                return OperatorStatus.ERROR
            else:
                return OperatorStatus.DONE
        else:
            return OperatorStatus.RUNNING

    def start(self) -> None:
        self.task = asyncio.create_task(self._run_handler())

    async def _run_handler(self) -> None:
        try:
            await self.run()
        except Exception as error:
            logger.exception(error, exc_info=True, stack_info=True)
            raise

    @abstractmethod
    async def run(self) -> None:  # pragma: no coverage
        raise NotImplementedError


class sum_2(AbstractOperator):
    async def run(self) -> None:
        print("start")
        var_name1, value1 = await self.inputs.get()
        if var_name1 != "a":
            raise NameError(f"Unknown variable {var_name1}")
        var_name2, value2 = await self.inputs.get()
        if var_name2 != "b":
            raise NameError(f"Unknown variable {var_name1}")

        await self.inputs.put(("c", value1 + value2))
