from enum import StrEnum


class QueueEngine(StrEnum):
    LOCAL = "local"
    RABBITMQ = "rabbitmq"


class JobStatus(StrEnum):
    PREPARING = "preparing"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    ABORTED = "aborted"


class OperatorStatus(StrEnum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    ERROR = "error"
    DONE = "done"
    ABORTED = "aborted"
