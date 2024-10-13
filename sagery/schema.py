from pydantic import BaseModel

from sagery.enums import VarStatus


class Object(BaseModel):
    """
    Model for representing an object.
    """
    data: dict[str, str]
    index: int


class Var(BaseModel):
    """
    Model for representing a var.
    """
    data: list[Object]
    accounted: bool
    status: VarStatus
