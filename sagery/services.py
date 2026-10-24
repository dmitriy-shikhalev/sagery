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
        job_id: int,
        **kwargs: dict[str, Any]
    ):
        self.job_repository = job_repository
        self.stream_repository = stream_repository
        self.value_repository = value_repository
        self.launch_repository = launch_repository
        self.job_id = job_id

    @abstractmethod
    async def run(self):
        raise NotImplementedError  # pragma: no cover


class JobService(AbstractService):
    def __init__(
        self,
        job_repository: JobRepository,
        stream_repository: StreamRepository,
        value_repository: ValueRepository,
        launch_repository: LaunchRepository,
        job_id: int,
        **kwargs: dict[str, Any]
    ):
        super().__init__(job_repository, stream_repository, value_repository, launch_repository, job_id, **kwargs)

    async def run(self):
        raise NotImplementedError


class StreamService(AbstractService):
    def __init__(
        self,
        job_repository: JobRepository,
        stream_repository: StreamRepository,
        value_repository: ValueRepository,
        launch_repository: LaunchRepository,
        job_id: int,
        **kwargs: dict[str, Any]
    ):
        super().__init__(job_repository, stream_repository, value_repository, launch_repository, job_id, **kwargs)
        self.operator_name = kwargs["operator_name"]

    async def run(self):
        raise NotImplementedError


class ValueService(AbstractService):  # TODO: нужен ли этот сервис?
    def __init__(
        self,
        job_repository: JobRepository,
        stream_repository: StreamRepository,
        value_repository: ValueRepository,
        launch_repository: LaunchRepository,
        job_id: int,
        **kwargs: dict[str, Any]
    ):
        super().__init__(job_repository, stream_repository, value_repository, launch_repository, job_id, **kwargs)
        self.operator_name = kwargs["operator_name"]

    async def run(self):
        raise NotImplementedError


class LaunchService(AbstractService):
    def __init__(
        self,
        job_repository: JobRepository,
        stream_repository: StreamRepository,
        value_repository: ValueRepository,
        launch_repository: LaunchRepository,
        job_id: int,
        **kwargs: Any,
    ):
        super().__init__(job_repository, stream_repository, value_repository, launch_repository, job_id, **kwargs)
        self.operator_name: str = kwargs["operator_name"]
        self.function = kwargs["function"]
        self.launch_id = kwargs["launch_id"]

    async def run(self):
        generator = self.function()
        anext(generator)

        job = await self.job_repository.get(self.job_id)
        streams = job.streams
        launch = await self.launch_repository.get(self.launch_id)

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

