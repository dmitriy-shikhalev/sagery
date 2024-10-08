from abc import ABC, abstractmethod


class AbstractFunction(ABC):
    # pylint: disable=missing-class-docstring
    # TODO: resolve, if descriptor here or just a function?
    @abstractmethod
    def run(self):
        """
        Run the function for execution.
        """
        raise NotImplementedError
