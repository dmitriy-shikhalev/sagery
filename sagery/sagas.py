from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Thread:  # noqa: D101
    name: str
    accounted: bool
    managed: bool


@dataclass(frozen=True)
class Function:  # noqa: D101
    name: str
    property: dict
    threads: list[str]
    operator: str


class AbstractSaga(ABC):
    """Abstract base class for sagas."""

    def __init__(self, job_id: int):  # noqa: D107
        self.job_id = job_id

    @property
    @abstractmethod
    def threads(self) -> list[Thread]:
        """Property should contain a list of Thread objects."""
        raise NotImplementedError

    @property
    @abstractmethod
    def functions(self) -> list[Function]:
        """Property should contain a list of functions objects."""
        raise NotImplementedError

    async def run(self) -> None:
        """Main function of Saga: implement long launch, with cycle inside, until job was finished."""  # noqa: D401
        raise NotImplementedError
