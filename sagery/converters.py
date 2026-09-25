from abc import ABC, abstractmethod

from sagery import domain, models


class AbstractConverter(ABC):
    @classmethod
    @abstractmethod
    def from_model_to_domain(cls, ):  # todo: define args and its types
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_domain_to_model(cls):  # todo: define args and its types
        raise NotImplementedError