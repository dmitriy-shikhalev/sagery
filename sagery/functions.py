from abc import ABC, abstractmethod


class AbstractFunction(ABC):
    # pylint: disable=too-few-public-methods
    """
    Abstract base class for all functions.
    """
    def __init__(self, *vars_: str, **kwargs):
        self.vars = vars_
        self.kwargs = kwargs

    @abstractmethod
    async def run(self):
        """
        Run the function for execution.
        """
        raise NotImplementedError
