from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sagery import domain
from sagery.converters import AbstractConverter, SagaConverter
from sagery.models import Saga

# from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value
from sagery.types import DBModel, DomainModel


class AbstractRepository[db_model_type: DBModel, domain_model_type: DomainModel, converter_class: AbstractConverter](
    ABC
):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[db_model_type]:
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def domain(self) -> type[domain_model_type]:
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def converter(self) -> type[converter_class]:
        raise NotImplementedError  # pragma: no cover

    async def create(self, domain_model: domain_model_type) -> domain_model_type:
        db_model = self.converter.from_domain_to_model(domain_model)
        self.session.add(db_model)

        await self.session.flush()
        domain_model.id = db_model.id
        return domain_model

    async def get(self, id: int) -> domain_model_type | None:
        stmt = select(self.model).where(self.model.id == id).limit(1)
        result = await self.session.execute(stmt)
        db_model = result.first()
        if db_model is None:
            return None
        return self.converter.from_model_to_domain(db_model)  # type: ignore

    async def filter(
        self, filter: Mapping[str, Any], limit: int | None = None, offset: int | None = None
    ) -> list[domain_model_type]:
        raise NotImplementedError

    async def update(self, id: int, **kwargs: Mapping[str, Any]) -> domain_model_type:
        raise NotImplementedError

    async def delete(self, id: int) -> domain_model_type:
        raise NotImplementedError


# Schema block


class SagaRepository(AbstractRepository[Saga, domain.Saga, SagaConverter]):
    model = Saga
    domain = domain.Saga
    converter = SagaConverter
