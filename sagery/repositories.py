from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, cast

from sqlalchemy import delete, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from sagery.models import Saga

# from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value
from sagery.types import DBModel


class AbstractRepository[db_model_type: DBModel](ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[db_model_type]:
        raise NotImplementedError  # pragma: no cover

    async def create(self, dict_: dict[str, Any]) -> db_model_type:
        db_model = self.model(**dict_)
        self.session.add(db_model)

        await self.session.flush()
        return db_model

    async def get(self, id: int) -> db_model_type | None:
        stmt = select(self.model).where(self.model.id == id).limit(1)
        result = await self.session.execute(stmt)
        db_model_obj = result.first()
        if db_model_obj is None:
            return None
        return db_model_obj  # type: ignore

    async def filter(
        self, filter_: Mapping[str, Any], *, limit: int | None = None, offset: int | None = None
    ) -> list[db_model_type]:
        stmt = select(self.model).filter_by(**filter_)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        db_model_list = result.all()

        return db_model_list  # type: ignore

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


class SagaRepository(AbstractRepository[Saga]):
    model = Saga
