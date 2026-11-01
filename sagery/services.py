import logging
from abc import ABC, abstractmethod

from typing import Any

from sagery.enums import Status
from sagery.repositories import JobRepository, LaunchRepository, StreamRepository, ValueRepository

logger = logging.getLogger(__name__)


class AbstractService(ABC):
    def __init__(
        self,
        job_repository: JobRepository,
        stream_repository: StreamRepository,
        value_repository: ValueRepository,
        launch_repository: LaunchRepository,
    ):
        self.job_repository = job_repository
        self.stream_repository = stream_repository
        self.value_repository = value_repository
        self.launch_repository = launch_repository

    @abstractmethod
    async def run(self, id: int) -> None:
        raise NotImplementedError  # pragma: no cover


class JobService(AbstractService):
    async def run(self, id: int) -> None:
        raise NotImplementedError


class StreamService(AbstractService):
    async def run(self, id: int) -> None:
        raise NotImplementedError


class ValueService(AbstractService):  # TODO: нужен ли этот сервис?
    async def run(self) -> None:
        raise NotImplementedError


class LaunchService(AbstractService):
    async def run(self, id: int) -> None:
        generator = self.function()
        anext(generator)

        launch = await self.launch_repository.get(id)

        for value in await self.value_repository.filter({"done": False}):
            await self.value_repository.update({"id": value.id}, {"launch_id": launch.id, "done": True})

            while True:
                try:
                    queue_name, data = await generator.asend((value.stream.queue_name, value.data))
                except StopAsyncIteration:
                    logger.info("Launch %s is over", launch.id)
                    await self.launch_repository.update(
                        {"id": launch.id, "status": Status.PROCESSING},
                        {"status": Status.DONE},
                    )
                    break
                except Exception as err:
                    logger.error("Unexpected error in launch %s: %s", launch.id, err)
                    await self.launch_repository.update(
                        {"id": launch.id, "status": Status.PROCESSING},
                        {"status": Status.FAILED},
                    )
                    break
                else:
                    raise NotImplementedError
