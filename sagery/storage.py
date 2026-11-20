import asyncio
import uuid

from sagery.enums import JobStatus
from sagery.manager import Manager
from sagery.models import Job, Saga, Stream


class Storage:
    def __init__(self, sagas_dict: dict[str, Saga]):
        self.sagas_dict = sagas_dict
        self._storage: dict[str, Job] = {}

    def __getitem__(self, key: str) -> Job:
        return self._storage[key]

    def create_job(self, saga_name: str, comment: str = "") -> str:
        job_id = str(uuid.uuid4())
        streams = {
            queue_name: Stream(queue_name=queue_name, values=[])
            for queue_name in self.sagas_dict[saga_name].queues
        }
        self._storage[job_id] = Job(
            id=job_id,
            saga_name=saga_name,
            status=JobStatus.PREPARING,
            comment=comment,
            streams=streams,
            manager=Manager(self.sagas_dict[saga_name], streams),
        )
        return job_id


