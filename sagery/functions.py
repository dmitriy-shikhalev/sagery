from abc import ABC, abstractmethod


class AbstractFunction(ABC):
    """Abstract base class for all functions."""

    def __init__(self, *vars_: str, **kwargs):  # noqa: D107
        self.vars = vars_
        self.kwargs = kwargs

    @abstractmethod
    async def run(self):
        """Run the function for execution."""
        raise NotImplementedError
