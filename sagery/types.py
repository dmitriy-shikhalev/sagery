"""
Модуль определяет собирательные типы моделей БД и доменных моделей
"""

from sagery import domain
from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value

DBModel = Job | Input | Launch | Operator | Output | Queue | Saga | Stream | Value
DomainModel = (
    domain.Job
    | domain.Launch
    | domain.Operator
    | domain.Saga
    | domain.Stream
    | domain.Queue
    | domain.Input
    | domain.Output
)
