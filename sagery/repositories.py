from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    """
    Abstract base class for repositories.
    """
    @abstractmethod
    async def create(self, **kwargs: Any) -> int:
        """
        Abstract method to create a new row in database.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Any:  # pylint: disable=redefined-builtin
        """
        Abstract method to get a row in database.
        """
        raise NotImplementedError

    @abstractmethod
    async def search(self, **kwargs: Any) -> list[Any]:
        """
        Abstract method to search rows in database.
        """
        raise NotImplementedError
