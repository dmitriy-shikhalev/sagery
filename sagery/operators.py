from abc import ABC, abstractmethod


class AbstractOperator(ABC):  # noqa: D101
    @property
    @abstractmethod
    def name(self) -> str:
        """Abstract operator name."""
        raise NotImplementedError

    @abstractmethod
    async def run(self):
        """Main operator action in this method."""  # noqa: D401
        raise NotImplementedError
