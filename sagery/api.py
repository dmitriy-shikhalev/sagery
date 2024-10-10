from fastapi import Depends, FastAPI  # , HTTPException
from sqlalchemy.orm import Session

from sagery.db import get_session
from sagery.schema import Var

app = FastAPI(title='Sagery API')


@app.post('/jobs/')
async def create_job(name: str, input: Var, session: Session = Depends(get_session)):
    # pylint: disable=redefined-builtin
    """
    API endpoint for creating jobs.
    """
    raise NotImplementedError


@app.get('/jobs/{id:int}/')
async def get_job_result(id: int, session: Session = Depends(get_session)):  # pylint: disable=redefined-builtin
    """
    API endpoint for getting job results.
    """
    raise NotImplementedError


@app.get('/jobs/{id:int}/status/')
async def get_job_status(id: int, session: Session = Depends(get_session)):  # pylint: disable=redefined-builtin
    """
    API endpoint for getting job current status.
    """
    raise NotImplementedError
