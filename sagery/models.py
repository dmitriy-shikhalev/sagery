import enum

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column, relationship)

from sagery.enums import VarStatus, Status, ObjectStatus


class Base(MappedAsDataclass, DeclarativeBase):
    # pylint: disable=too-few-public-methods
    """subclasses will be converted to dataclasses"""


class Item(Base):
    # pylint: disable=too-few-public-methods
    """
    Class for representing an item in the sagery database.
    """
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id"), nullable=False, index=True)
    object: Mapped["Object"] = relationship(back_populates="items")
    key: Mapped[str] = mapped_column(nullable=False, index=True)
    value: Mapped[str] = mapped_column(String(), nullable=False, default='null')


class Object(Base):
    # pylint: disable=too-few-public-methods
    """
    Class for representing an object in the sagery database.
    """
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    var_id: Mapped[int] = mapped_column(ForeignKey("vars.id"), nullable=False, index=True)
    var: Mapped["Var"] = relationship(back_populates="items")
    index: Mapped[int] = mapped_column(Integer(), nullable=False, index=True)

    items: Mapped[list[Item]] = relationship(
        Item,
        back_populates="object",
    )
    request: Mapped["Request"] = relationship("Request", back_populates="object")

    status: Mapped[ObjectStatus] = mapped_column(
        ENUM(ObjectStatus),
        default=ObjectStatus.NONE,
        nullable=False,
        index=True
    )


class Var(Base):
    # pylint: disable=too-few-public-methods
    """
    Class for representing a variable in the sagery database.
    """
    __tablename__ = "vars"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False, index=True)
    job: Mapped["Job"] = relationship(back_populates="branches")
    name: Mapped[str] = mapped_column(String(), nullable=False)

    objects: Mapped[list[Object]] = relationship(Object, back_populates="var")
    status: Mapped[VarStatus] = mapped_column(ENUM(VarStatus), default=VarStatus.STARTED, nullable=False, index=True)

    __table_args__ = (
        Index("uix_job_var", 'job_id', "name", unique=True),
    )


class Request(Base):
    """
    Class for representing a request in the sagery database.
    """
    # pylint: disable=too-few-public-methods
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id"), nullable=False, unique=True)
    object: Mapped["Object"] = relationship(back_populates="request")

    operator_name: Mapped[str] = mapped_column(String(), nullable=False, index=True)
    status: Mapped[Status] = mapped_column(ENUM(Status), default=Status.PENDING, nullable=False, index=True)


class Job(Base):
    # pylint: disable=too-few-public-methods
    """
    Class for representing a job in the sagery database.
    """
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    vars: Mapped[list[Var]] = relationship(back_populates="job")
    requests: Mapped[list["Request"]] = relationship(back_populates="job")
    status: Mapped[Status] = mapped_column(ENUM(Status), default=Status.PENDING, nullable=False, index=True)
