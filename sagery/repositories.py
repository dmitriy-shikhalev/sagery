from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value

ModelClass = Job | Input | Launch | Operator | Output | Queue | Saga | Stream | Value


class AbstractRepository[Object: type[ModelClass]](ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[ModelClass]:
        raise NotImplementedError

    def create(self, **kwargs: Mapping[Any, Any]) -> Object:
        raise NotImplementedError

    def get(self, id: int) -> Object:
        raise NotImplementedError

    def update(self, id: int, **kwargs: Mapping[Any, Any]) -> Object:
        raise NotImplementedError

    def delete(self, id: int) -> Object:
        raise NotImplementedError


# Schema block


class SagaRepository(AbstractRepository):
    model = Saga
