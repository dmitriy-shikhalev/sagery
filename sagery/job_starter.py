from sqlalchemy.ext.asyncio import AsyncEngine

from sagery.settings import JobStarterSettings


class JobStarter:
    def __init__(self, engine: AsyncEngine, settings: JobStarterSettings):
        self.engine = engine
        self.count = 0
        self.max_count = settings.max_count
        self.sleep_time = settings.sleep_time
        self.job_coroutines = []

    async def start(self):
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError
