from abc import ABC, abstractmethod

from typing import Any

from sagery.repositories import JobRepository, LaunchRepository, StreamRepository, ValueRepository


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
        **kwargs: dict[str, Any]
    ):
        super().__init__(job_repository, stream_repository, value_repository, launch_repository, job_id, **kwargs)
        self.operator_name = kwargs["operator_name"]

    async def run(self):
        raise NotImplementedError