import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from sagery.enums import OperatorStatus

logger = logging.getLogger(__name__)


class AbstractOperator(ABC):
    task: asyncio.Task | None = None
    queue_task: asyncio.Task | None = None
    time: int | None = None

    def __init__(
        self,
        queues: dict[str, asyncio.Queue[Any]],
        timeout: float | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        self._queues = queues
        self.timeout = timeout
        self.kwargs = kwargs

    @property
    def queues(self) -> dict[str, asyncio.Queue[Any]]:
        return self._queues

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

    async def start(self) -> None:
        if self.task is not None:
            raise ValueError(f"Try to start operator {self}, that has already started!")
        self.task = asyncio.create_task(self._run_handler())

    async def _run_handler(self) -> None:
        try:
            async with asyncio.timeout(self.time):
                await self.run()
        except Exception as error:
            logger.exception(error, exc_info=True, stack_info=True)
            raise

    @abstractmethod
    async def run(self) -> None:  # pragma: no coverage
        raise NotImplementedError


class sum_2(AbstractOperator):
    async def run(self) -> None:
        logger.info("Start sum_2 operator")
        value1 = await self.queues["a"].get()
        value2 = await self.queues["b"].get()

        await self.queues["c"].put(value1 + value2)
