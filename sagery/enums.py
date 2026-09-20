from enum import StrEnum


class Status(StrEnum):
    PREPARING = "preparing"
    PROCESSING = "processing"
    DONE = "DONE"
    FAILED = "failed"
    ABORTED = "aborted"
