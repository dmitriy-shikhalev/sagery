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
        input_queues: dict[str, asyncio.Queue[Any]],
        output_queues: dict[str, asyncio.Queue[Any]],
        time: int | None = None,
    ) -> None:
        self.time = time
        self.input_queues = input_queues
        self.output_queues = output_queues
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

    async def start(self) -> None:
        if self.task is not None:
            raise ValueError(f"Try to start operator {self}, that has already started!")
        self.task = asyncio.create_task(self._run_handler())

    @staticmethod
    async def queue_getter(queue_name: str, queue: Queue[Any]) -> None:
        """
        Вспомогательная функция - получает значение из очереди
        и возвращает его вместе с номером очереди,
        чтобы мы понимали, откуда оно пришло
        """
        return queue_name, await queue.get()

    @staticmethod
    async def queue_processer():
        waiting_tasks = {i: asyncio.create_task(queue_getter(i, queue)) for i, queue in enumerate(queues)}
        while True:
            done, _pending = await asyncio.wait(waiting_tasks.values(), return_when=asyncio.FIRST_COMPLETED)
            for finished_task in done:
                i, result = await finished_task
                print(f"Got item {result} from queue {i}")
                waiting_tasks[i] = asyncio.create_task(queue_getter(i, queues[i]))

    async def main():  ???
        producers = [asyncio.create_task(producer(queue1, 1)), asyncio.create_task(producer(queue2, 1.5))]
        processor = asyncio.create_task(queue_processer())
        tasks = producers + [processor]
        await asyncio.gather(*tasks)

    async def _processing_queues(self) -> None:
        raise NotImplementedError

    asyncio.run(main())
    raise NotImplementedError

    async def _run_handler(self) -> None:
        self.queue_task = asyncio.create_task(self._processing_queues())
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
        var_name1, value1 = await self.inputs.get()
        if var_name1 != "a":
            raise NameError(f"Unknown variable {var_name1}")
        var_name2, value2 = await self.inputs.get()
        if var_name2 != "b":
            raise NameError(f"Unknown variable {var_name1}")

        await self.outputs.put(("c", value1 + value2))
