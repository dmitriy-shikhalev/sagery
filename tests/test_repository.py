from sagery.repositories import JobRepository


async def test_job_create(test_session):
    """
    Test of JobRepository class, method "create".
    """
    job_repository = JobRepository(test_session)
    job_id = await job_repository.create(a='b')

    read_job = await job_repository.search(id=job_id)

    assert read_job.a == 'b'
