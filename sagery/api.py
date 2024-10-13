from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sagery.db import get_session
from sagery.models import Job
from sagery.registry import job_registry
from sagery.repositories import JobRepository

app = FastAPI(title='Sagery API')


@app.post('/jobs/{name}/', response_model=int, status_code=201)
async def create_job(name: str, session: Session = Depends(get_session)):
    # pylint: disable=redefined-builtin
    """
    API endpoint for creating jobs.
    """
    if job_registry.get(name) is None:
        raise HTTPException(status_code=404, detail=f'Job {name} not found')

    job_repository = JobRepository(session)
    job: Job = await job_repository.create(name=name)
    return job.id


@app.get('/jobs/{job_id:int}/')
async def get_job(job_id: int, session: Session = Depends(get_session)):
    """
    API endpoint for getting job results.
    """
    raise NotImplementedError


@app.get('/jobs/{job_id:int}/vars/')
async def get_var_list(job_id: int, session: Session = Depends(get_session)):
    """
    API endpoint for getting vars for job.
    """
    raise NotImplementedError


@app.post('/jobs/{job_id:int}/vars/{var_name:str}/set-closed/')
async def set_var_closed(job_id: int, var_name: str, session: Session = Depends(get_session)):
    """
    API endpoint for setting the closed var for job.
    """
    raise NotImplementedError


@app.get('/jobs/{job_id:int}/vars/{var_name:str}/')
async def get_one_var(job_id: int, var_name: str, session: Session = Depends(get_session)):
    """
    API endpoint for getting one var for job by var name.
    """
    raise NotImplementedError


@app.post('/jobs/{job_id:int}/vars/{var_name}/objects/')
async def add_object(job_id: int, var_name: str, session: Session = Depends(get_session)):
    """
    API endpoint for adding object to var.
    """
    raise NotImplementedError


@app.get('/jobs/{job_id:int}/vars/{var_name}/objects/')
async def get_object_list(job_id: int, var_name: str, session: Session = Depends(get_session)):
    """
    API endpoint for adding object to var.
    """
    raise NotImplementedError


@app.get('/jobs/{job_id:int}/vars/{var_name}/objects/{index:int}/')
async def get_one_object(job_id: int, var_name: str, index: int, session: Session = Depends(get_session)):
    """
    API endpoint for adding object to var.
    """
    raise NotImplementedError
