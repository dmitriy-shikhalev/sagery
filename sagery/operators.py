from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractOperator(ABC):
    # pylint: disable=missing-class-docstring
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Abstract operator name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def input(self) -> BaseModel:
        """
        Abstract field for input type.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def output(self) -> BaseModel:
        """
        Abstract field for output type.
        """
        raise NotImplementedError

    @abstractmethod
    async def run(self):
        """
        Main operator action in this method.
        """
        raise NotImplementedError
