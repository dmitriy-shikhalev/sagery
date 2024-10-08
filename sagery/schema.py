from pydantic import BaseModel, RootModel


class Object(RootModel):
    root: dict[str, str]


class Var(RootModel):
    root: list[Object]
