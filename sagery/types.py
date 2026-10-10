"""
Модуль определяет собирательные типы моделей БД
"""

from sagery.models import Input, Job, Launch, Operator, Output, Queue, Saga, Stream, Value

DBModel = Job | Input | Launch | Operator | Output | Queue | Saga | Stream | Value
