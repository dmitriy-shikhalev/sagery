from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, cast

from sqlalchemy import delete, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from sagery.models import Job, Launch, Stream, Value
from sagery.types import DBModel


class AbstractRepository[db_model_type: DBModel](ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[db_model_type]:
        raise NotImplementedError  # pragma: no cover

    async def create(self, dict_: dict[str, Any]) -> dict[str, Any]:
        db_model = self.model(**dict_)
        self.session.add(db_model)

        await self.session.flush()
        return db_model.as_dict()

    async def get(self, id: int) -> dict[str, Any] | None:
        stmt = select(self.model).where(self.model.id == id).limit(1)
        result = await self.session.execute(stmt)
        db_model_obj = result.first()
        if db_model_obj is None:
            return None
        return db_model_obj.as_dict()  # type: ignore[no-any-return]

    async def filter(
        self, filter_: Mapping[str, Any], *, limit: int | None = None, offset: int | None = None
    ) -> list[dict[str, Any]]:
        stmt = select(self.model).filter_by(**filter_)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        db_model_list = result.all()

        return [obj.as_dict() for obj in db_model_list]

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


class JobRepository(AbstractRepository[Job]):
    model = Job


class StreamRepository(AbstractRepository[Stream]):
    model = Stream


class ValueRepository(AbstractRepository[Value]):
    model = Value


class LaunchRepository(AbstractRepository[Launch]):
    model = Launch
