from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, cast

from sqlalchemy import delete, select, update
from sqlalchemy.engine import CursorResult
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
        db_model_obj = result.first()
        if db_model_obj is None:
            return None
        return self.converter.from_model_to_domain(db_model_obj)  # type: ignore

    async def filter(
        self, filter_: Mapping[str, Any], *, limit: int | None = None, offset: int | None = None
    ) -> list[domain_model_type]:
        stmt = select(self.model).filter_by(**filter_)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        db_model_list = result.all()

        domain_object_list = []
        for db_model_obj in db_model_list:
            domain_object = self.converter.from_model_to_domain(db_model_obj)  # type: ignore
            domain_object_list.append(domain_object)

        return domain_object_list

    async def update(self, filter_: Mapping[str, Any], values: Mapping[str, Any]) -> int:
        stmt = update(self.model).filter_by(**filter_).values(**values)
        result = cast(CursorResult[Any], await self.session.execute(stmt))
        return result.rowcount

    async def delete(self, filter_: Mapping[str, Any]) -> int:
        if not filter_:
            raise ValueError("Don't use .delete({}). You try to remove all rows!")
        stmt = delete(self.model).filter_by(**filter_)
        result = cast(CursorResult[Any], await self.session.execute(stmt))
        return result.rowcount


# Schema block


class SagaRepository(AbstractRepository[Saga, domain.Saga, SagaConverter]):
    model = Saga
    domain = domain.Saga
    converter = SagaConverter
