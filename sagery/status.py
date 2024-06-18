from enum import Enum


class JobStatus(Enum):
    PENDING = 'NEW'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'


class RequestStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'
