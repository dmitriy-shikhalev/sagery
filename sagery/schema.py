from pydantic import RootModel


class Object(RootModel):
    """
    Model for representing object.
    """
    root: dict[str, str]


class Var(RootModel):
    """
    Model for representing var.
    """
    root: list[Object]
