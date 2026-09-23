from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from sagery import domain
from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value

ModelClass = Job | Input | Launch | Operator | Output | Queue | Saga | Stream | Value
DomainModel = domain.Job | domain.Launch | domain.Operator | domain.Saga | domain.Stream


class AbstractRepository[Object: type[ModelClass], domain_model: type[DomainModel]](ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[ModelClass]:
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def domain(self) -> type[DomainModel]:
        raise NotImplementedError  # pragma: no cover

    async def create(self, **kwargs: Any) -> Object:
        self.session.add(self.model(**kwargs))

    async def get(self, id: int) -> Object:
        raise NotImplementedError

    async def update(self, id: int, **kwargs: Mapping[Any, Any]) -> Object:
        raise NotImplementedError

    async def delete(self, id: int) -> Object:
        raise NotImplementedError


# Schema block


class SagaRepository(AbstractRepository):
    model = Saga
    domain = domain.Saga
