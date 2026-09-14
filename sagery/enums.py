from enum import Enum


class Status(str, Enum):
    PREPARING = "preparing"
    PROCESSING = "processing"
    DONE = "DONE"
    FAILED = "failed"
    ABORTED = "aborted"
