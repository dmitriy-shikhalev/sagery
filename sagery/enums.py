from enum import Enum, StrEnum


class Mode(StrEnum):
    """
    Mode types.
    """
    WEB = 'web'
    CORE = 'core'


# DB enums
class Status(Enum):
    """
    All possible statuses for jobs and requests.
    """
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'


class ObjectStatus(Enum):
    """
    All possible object statuses.
    """
    NONE = 'NONE'
    USED = 'USED'


class ThreadStatus(Enum):
    """
    All possible Thread statuses.
    """
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
