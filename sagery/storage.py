import asyncio
import uuid

from sagery.enums import JobStatus
from sagery.operators import AbstractOperator
from sagery.schema import Saga


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
