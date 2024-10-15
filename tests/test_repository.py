from sagery.repositories import JobRepository


async def test_job_create_with_filter_by(test_session):
    """
    Test of JobRepository class, method "create".
    """
    job_repository = JobRepository(test_session)
    job = await job_repository.create(name='test name')

    read_jobs = await job_repository.filter_by(id=job.id)

    assert len(read_jobs) == 1
    assert read_jobs[0].name == 'test name'
    assert read_jobs[0].status.value == 'PENDING'


async def test_job_create_with_get(test_session):
    """
    Test of JobRepository class, method "create".
    """
    job_repository = JobRepository(test_session)
    job = await job_repository.create(name='test name')

    read_job = await job_repository.get(job.id)

    assert read_job.name == 'test name'
    assert read_job.status.value == 'PENDING'
