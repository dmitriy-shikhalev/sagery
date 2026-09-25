from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from sagery import domain
from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value
from sagery.types import DBModel, DomainModel


class AbstractRepository[db_model_type: type[DBModel], domain_model_type: type[DomainModel]](ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> db_model_type:
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def domain(self) -> domain_model_type:
        raise NotImplementedError  # pragma: no cover

    async def create(self, **kwargs: Any) -> domain_model_type:
        model = self.model(**kwargs)
        self.session.add(model)
        return model

    async def get(self, id: int) -> domain_model_type:
        raise NotImplementedError

    async def update(self, id: int, **kwargs: Mapping[Any, Any]) -> domain_model_type:
        raise NotImplementedError

    async def delete(self, id: int) -> domain_model_type:
        raise NotImplementedError


# Schema block


class SagaRepository(AbstractRepository):
    model = Saga
    domain = domain.Saga
