import asyncio
import uuid

from sagery.enums import JobStatus
from sagery.operators import AbstractOperator
from sagery.schema import Saga


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

        queues: dict[str, asyncio.Queue] = {queue_name: asyncio.Queue() for queue_name in saga.queues}
        operator_saga_dict = dict(saga.operators.items())

        self.queues = queues
        self.operator_saga_dict = operator_saga_dict
        self.operators: dict[str, AbstractOperator] = {}

    async def run(self) -> None:
        raise NotImplementedError  # pragma: no cover

    async def start(self) -> None:
        for operator_saga in self.operator_saga_dict.values():
            operator = operator_saga.operator_cls(self.queues)
            await operator.start()

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
        self._storage[job.id] = job
        return job.id
