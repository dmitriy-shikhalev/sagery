"""
Модуль определяет собирательные типы моделей БД
"""

from sagery.models import Job, Launch, Stream, Value

DBModel = Job | Launch | Stream | Value
