from sagery.jobs import Job
from sagery.schema import Saga


class Storage:
    def __init__(self, sagas_dict: dict[str, Saga]):
        self.sagas_dict = sagas_dict
        self._storage: dict[str, Job] = {}

    def create_job(self, saga_name: str, comment: str) -> str:
        saga = self.sagas_dict[saga_name]
        job = Job(saga, comment)
        self._storage[job.id] = job
        return job.id

    def get_job(self, job_id: str) -> Job:
        return self._storage[job_id]

    def set_processing_job(self, job_id: str) -> Job:
        raise NotImplementedError

    def cancel_job(self, job_id: str) -> Job:
        raise NotImplementedError

    def delete_job(self, job_id: str) -> None:
        raise NotImplementedError
