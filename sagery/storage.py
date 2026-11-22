import asyncio
import uuid

from sagery.enums import JobStatus
from sagery.manager import Manager
from sagery.schema import Job, Saga, Stream, Operator
from sagery.operators import AbstractOperator


class Launch:
    def __init__(self, inputs: list[str], outputs: list[str], object: AbstractOperator) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.object = object

    async def start(self) -> None:
        await self.object.start()


class Job:
    task: asyncio.Task | None = None

    def __init__(self, saga: Saga, comment: str):
        self.id = uuid.uuid4().hex
        self.saga = saga
        self.comment = comment
        self.status = JobStatus.PREPARING

        streams = {
            queue_name: asyncio.Queue()
            for queue_name in sagas.queues
        }
        launches = {
            name: operator.object()
            for name, operator in saga.operators.items()
        }

        self.streams = streams
        self.launches = launches

    async def run(self) -> None:
        raise NotImplementedError

    async def start(self) -> None:
        self._task = asyncio.create_task(self.run())


class Storage:
    def __init__(self, sagas_dict: dict[str, Saga]):
        self.sagas_dict = sagas_dict
        self._storage: dict[str, Job] = {}

    def __getitem__(self, key: str) -> Job:
        return self._storage[key]

    def create_job(self, saga_name: str, comment: str) -> str:
        saga = self.sagas_dict[saga_name]
        job = Job(saga, comment)
        return job.id


