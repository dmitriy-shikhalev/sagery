import enum

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, JSON
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column, relationship)


class Status(enum.Enum):
    """
    All possible statuses.
    """
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'


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
    var_id: Mapped[int] = mapped_column(ForeignKey("vars.id"), nullable=False, index=True)
    var: Mapped["Var"] = relationship(back_populates="items")
    index: Mapped[int] = mapped_column(Integer(), nullable=False, index=True)
    key: Mapped[str] = mapped_column(nullable=False, index=True)
    value: Mapped[str] = mapped_column(JSON(), nullable=False, default='null')


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

    items: Mapped[list[Item]] = relationship(Item, back_populates="var")
    requests: Mapped[list["Request"]] = relationship("Request", back_populates="var")

    __table_args__ = (
        Index("uix_job_var", 'job_id', "name", unique=True),
    )


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


class Request(Base):
    """
    Class for representing a request in the sagery database.
    """
    # pylint: disable=too-few-public-methods
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False, index=True)
    job: Mapped["Job"] = relationship(back_populates="requests")
    var_id: Mapped[int] = mapped_column(ForeignKey("vars.id"), nullable=False, index=True)
    var: Mapped["Var"] = relationship(back_populates="requests")

    index: Mapped[int] = mapped_column(Integer(), nullable=False, index=True)
    operator_name: Mapped[str] = mapped_column(String(), nullable=False, index=True)
    status: Mapped[Status] = mapped_column(ENUM(Status), default=Status.PENDING, nullable=False, index=True)
