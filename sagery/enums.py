from enum import StrEnum


class Status(StrEnum):
    PREPARING = "preparing"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    ABORTED = "aborted"


class StreamStatus(StrEnum):
    NEW = "new"
    CLOSED = "closed"
    COMPLETED = "completed"


class OperatorStatus(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    DONE = "DONE"
    ABORTED = "ABORTED"
