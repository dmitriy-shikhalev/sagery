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