from enum import Enum


class JobStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'
    ROLLINGBACK = 'ROLLINGBACK'
    ROLLEDBACK = 'ROLLEDBACK'


class RequestStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'
