from abc import ABC, abstractmethod


class AbstractOperator(ABC):  # or use Protocol?
    pass


class AbstractFunction(ABC):
    # TODO: resolve, if descriptor here or just a function?
    @abstractmethod
    def run(self):
        raise NotImplementedError


class AbstractJob(ABC):
    pass


from itertools import permutations
permutations()