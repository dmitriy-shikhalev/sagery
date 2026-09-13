from enum import Enum


class JobStatus(str, Enum):
    PREPARING = "preparing"
    PROCESSING = "processing"
    DONE = "DONE"
    FAILED = "failed"
    ABORTED = "aborted"


class LaunchStatus(str, Enum):
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    ABORTED = "aborted"
