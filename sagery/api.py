from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sagery.db import get_session
from sagery.models import Job
from sagery.registry import SAGA_REGISTRY
from sagery.repositories import JobRepository, ThreadRepository

app = FastAPI(title="Sagery API")


@app.post("/sagas/{name}/", response_model=int, status_code=201)
async def create_job(name: str, session: Session = Depends(get_session)):
    """API endpoint for creating jobs."""  # noqa: D401
    saga = SAGA_REGISTRY.get(name)
    if saga is None:
        raise HTTPException(status_code=404, detail=f"Saga {name} not found")

    job_repository = JobRepository(session)
    thread_repository = ThreadRepository(session)

    job: Job = await job_repository.create(name=name)
    for thread in saga.threads:
        await thread_repository.create(job_id=job.id, name=thread.name, accounted=thread.accounted)

    raise NotImplementedError  # todo: create all FunctionCalls

    session.commit()
    return job.id


@app.get("/jobs/{job_id:int}/")
async def get_job(job_id: int, session: Session = Depends(get_session)):
    """API endpoint for getting job results."""  # noqa: D401
    raise NotImplementedError


@app.get("/jobs/{job_id:int}/threads/")
async def get_thread_list(job_id: int, session: Session = Depends(get_session)):
    """API endpoint for getting threads for job."""  # noqa: D401
    raise NotImplementedError


@app.post("/jobs/{job_id:int}/threads/{thread_name:str}/set-closed/")
async def set_thread_closed(job_id: int, thread_name: str, session: Session = Depends(get_session)):
    """API endpoint for setting the closed thread for job."""  # noqa: D401
    raise NotImplementedError


@app.get("/jobs/{job_id:int}/threads/{thread_name:str}/")
async def get_one_thread(job_id: int, thread_name: str, session: Session = Depends(get_session)):
    """API endpoint for getting one thread for job by thread name."""  # noqa: D401
    raise NotImplementedError


@app.post("/jobs/{job_id:int}/threads/{thread_name}/objects/")
async def add_object(
    job_id: int, thread_name: str, index: int, object_data: dict[str, str], session: Session = Depends(get_session)
):
    """API endpoint for adding object to thread."""  # noqa: D401
    raise NotImplementedError


@app.get("/jobs/{job_id:int}/threads/{thread_name}/objects/")
async def get_object_list(job_id: int, thread_name: str, session: Session = Depends(get_session)):
    """API endpoint for adding object to thread."""  # noqa: D401
    raise NotImplementedError


@app.get("/jobs/{job_id:int}/threads/{thread_name}/objects/{index:int}/")
async def get_one_object(job_id: int, thread_name: str, index: int, session: Session = Depends(get_session)):
    """API endpoint for adding object to thread."""  # noqa: D401
    raise NotImplementedError
