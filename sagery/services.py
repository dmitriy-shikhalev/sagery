import logging
from abc import ABC, abstractmethod

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
