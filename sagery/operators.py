from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractOperator(ABC):  # todo: or use Protocol?
    # pylint: disable=missing-class-docstring
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