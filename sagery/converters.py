from abc import ABC, abstractmethod

from sagery import domain, models
from sagery.types import DBModel, DomainModel


class AbstractConverter[db_model_type: DBModel, domain_model_type: DomainModel](ABC):
    @classmethod
    @abstractmethod
    def from_model_to_domain(cls, db_model: db_model_type) -> domain_model_type:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_domain_to_model(cls, domain_model: domain_model_type) -> db_model_type:
        raise NotImplementedError


class SagaConverter(AbstractConverter[models.Saga, domain.Saga]):
    @classmethod
    def from_model_to_domain(cls, db_model: models.Saga) -> domain.Saga:
        return domain.Saga(
            id=db_model.id,
            name=db_model.name,
            comment=db_model.comment,
            queues={queue.name: QueueConverter.from_model_to_domain(queue) for queue in db_model.queues},
            operators={
                operator.name: OperatorConverter.from_model_to_domain(operator) for operator in db_model.operators
            },
        )

    @classmethod
    def from_domain_to_model(cls, domain_model: domain.Saga) -> models.Saga:
        """
        Очереди и Операторы не преобразуются в модели автоматически,
        потому что иначе нельзя будет использовать данный метод для
        изменения модели в БД.
        """
        return models.Saga(
            id=domain_model.id,
            name=domain_model.name,
            comment=domain_model.comment,
        )


class QueueConverter(AbstractConverter[models.Queue, domain.Queue]):
    @classmethod
    def from_model_to_domain(cls, db_model: models.Queue) -> domain.Queue:
        return domain.Queue(id=db_model.id, name=db_model.name)

    @classmethod
    def from_domain_to_model(cls, domain_model: domain.Queue) -> models.Queue:
        return models.Queue(id=domain_model.id, name=domain_model.name)


class OperatorConverter(AbstractConverter[models.Operator, domain.Operator]):
    @classmethod
    def from_model_to_domain(cls, db_model: models.Operator) -> domain.Operator:
        return domain.Operator(
            id=db_model.id,
            name=db_model.name,
            inputs=[InputConverter.from_model_to_domain(input_) for input_ in db_model.inputs],
            outputs=[OutputConverter.from_model_to_domain(output_) for output_ in db_model.outputs],
        )

    @classmethod
    def from_domain_to_model(cls, domain_model: domain.Operator) -> models.Operator:
        """
        Входы и Выходы не преобразуются в модели автоматически,
        потому что иначе нельзя будет использовать данный метод для
        изменения модели в БД.
        """
        return models.Operator(
            id=domain_model.id,
            name=domain_model.name,
        )


class InputConverter(AbstractConverter[models.Input, domain.Input]):
    @classmethod
    def from_model_to_domain(cls, db_model: models.Input) -> domain.Input:
        return domain.Input(id=db_model.id, operator_id=db_model.operator_id, queue_id=db_model.queue_id)

    @classmethod
    def from_domain_to_model(cls, domain_model: domain.Input) -> models.Input:
        return models.Input(id=domain_model.id, operator_id=domain_model.operator_id, queue_id=domain_model.queue_id)


class OutputConverter(AbstractConverter[models.Output, domain.Output]):
    @classmethod
    def from_model_to_domain(cls, db_model: models.Output) -> domain.Output:
        return domain.Output(id=db_model.id, operator_id=db_model.operator_id, queue_id=db_model.queue_id)

    @classmethod
    def from_domain_to_model(cls, domain_model: domain.Output) -> models.Output:
        return models.Output(id=domain_model.id, operator_id=domain_model.operator_id, queue_id=domain_model.queue_id)
