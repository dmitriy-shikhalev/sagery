from enum import StrEnum


class Status(StrEnum):
    PREPARING = "preparing"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    ABORTED = "aborted"
