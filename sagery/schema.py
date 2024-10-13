from pydantic import BaseModel, RootModel


class Object(RootModel):
    """
    Model for representing object.
    """
    root: dict[str, str]


class Var(BaseModel):
    """
    Model for representing var.
    """
    data: list[Object]
    closed: bool
