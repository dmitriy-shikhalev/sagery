from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import TableClause

from sagery.models import Job


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
        raise NotImplementedError

    def __init__(self, session: Session) -> None:
        self.session = session

    async def create(self, **kwargs: Any) -> int:
        """
        Common method to create a new row in database of self.model.
        """
        statement = insert(self.model).values(**kwargs)
        result = self.session.execute(statement)
        return result.returns_rows[0].id

    async def get(self, id: int) -> Any:  # pylint: disable=redefined-builtin
        """
        Common method to get a row in database of self.model.
        """
        raise NotImplementedError

    async def search(self, **kwargs: Any) -> list[Any]:
        """
        Common method to search rows in database of self.model.
        """
        raise NotImplementedError


class JobRepository(AbstractRepository):
    """
    Class for repository for Jobs.
    """
    model = Job  # type: ignore
