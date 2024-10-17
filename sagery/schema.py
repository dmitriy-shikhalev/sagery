from pydantic import BaseModel

from sagery.enums import ThreadStatus


class Object(BaseModel):
    """Model for representing an object."""

    data: dict[str, str]
    index: int


class Thread(BaseModel):
    """Model for representing a var."""

    data: list[Object]
    accounted: bool
    status: ThreadStatus
