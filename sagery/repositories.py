from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import TableClause

from sagery.models import Item, Job, Object, Request, Thread


class AbstractRepository(ABC):
    """
    Abstract base class for repositories.
    """
    @property
    @abstractmethod
    def model(self) -> TableClause:
        """
        Property, that contains sqlalchemy model.
        """
        raise NotImplementedError  # pragma: no cover

    def __init__(self, session: Session) -> None:
        self.session = session

    async def create(self, **kwargs: Any) -> Job:
        """
        Common method to create a new row in database of self.model.
        """
        statement = insert(self.model).values(**kwargs).returning(self.model)
        result = self.session.execute(statement)
        return result.scalar()

    async def get(self, id: int) -> Any:  # pylint: disable=redefined-builtin
        """
        Common method to get a row in database of self.model.
        """
        statement = select(self.model).filter(self.model.id == id)  # type: ignore[attr-defined]
        result = self.session.execute(statement)
        return result.scalar()

    async def search(self, **kwargs: Any) -> list[Any]:
        """
        Common method to search rows in database of self.model.
        """
        statement = select(self.model).filter_by(**kwargs)
        result = self.session.execute(statement)
        return result.scalars().fetchall()  # type: ignore


class JobRepository(AbstractRepository):
    """
    Class for repository for Jobs.
    """
    model = Job  # type: ignore


class ThreadRepository(AbstractRepository):
    """
    Class for repository for Vars.
    """
    model = Thread  # type: ignore


class ObjectRepository(AbstractRepository):
    """
    Class for repository for Objects.
    """
    model = Object  # type: ignore


class ItemRepository(AbstractRepository):
    """
    Class for repository for Items.
    """
    model = Item  # type: ignore


class RequestRepository(AbstractRepository):
    """
    Class for repository for Requests.
    """
    model = Request  # type: ignore
