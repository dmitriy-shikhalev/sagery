from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractOperator(ABC):  # todo: or use Protocol?
    # pylint: disable=missing-class-docstring
    @property
    @abstractmethod
    def input(self) -> BaseModel:
        raise NotImplementedError

    @property
    @abstractmethod
    def output(self) -> BaseModel:
        raise NotImplementedError


class AbstractFunction(ABC):
    # pylint: disable=missing-class-docstring
    # TODO: resolve, if descriptor here or just a function?
    @abstractmethod
    def run(self):
        """
        Run the function for execution.
        """
        raise NotImplementedError


class AbstractJob(ABC):
    # pylint: disable=missing-class-docstring
    pass
