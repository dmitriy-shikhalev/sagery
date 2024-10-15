from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Thread:
    # pylint: disable=missing-class-docstring
    name: str
    accounted: bool
    managed: bool


class AbstractSaga(ABC):
    """
    Abstract base class for sagas.
    """
    def __init__(self, job_id: int):
        self.job_id = job_id

    @property
    @abstractmethod
    def thread_list(self) -> list[Thread]:
        """
        Property should contain a list of Thread objects.
        """
        raise NotImplementedError

    async def run(self) -> None:
        """
        Main function of Saga: implement long launch, with cycle inside, until job finishes.
        """
        raise NotImplementedError
