from datetime import datetime
from typing import Any

from sqlalchemy import CHAR, TEXT, Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sagery.db import Base
from sagery.enums import Status

# Block Schema


class Saga(Base):
    __tablename__ = "sagas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(CHAR(50), nullable=True, unique=True)
    comment: Mapped[str] = mapped_column(TEXT(), nullable=True)

    queues: Mapped[list["Queue"]] = relationship(back_populates="saga")
    operators: Mapped[list["Operator"]] = relationship(back_populates="saga")
    jobs: Mapped[list["Job"]] = relationship(back_populates="saga")


class Queue(Base):
    __tablename__ = "queues"
    __table_args__ = (UniqueConstraint("saga_id", "name", name="uq_queue"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    saga_id: Mapped[int] = mapped_column(ForeignKey("sagas.id"), nullable=False)
    name: Mapped[str] = mapped_column(CHAR(50), nullable=False, index=True)

    saga: Mapped["Saga"] = relationship(back_populates="queues")
    streams: Mapped[list["Stream"]] = relationship(back_populates="queue")
    inputs: Mapped[list["Input"]] = relationship(back_populates="queue")
    outputs: Mapped[list["Output"]] = relationship(back_populates="queue")


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    saga_id: Mapped[int] = mapped_column(ForeignKey("sagas.id"), nullable=False)
    name: Mapped[str] = mapped_column(CHAR(50), nullable=False, index=True)

    saga: Mapped[Saga] = relationship(back_populates="operators")
    inputs: Mapped[list["Input"]] = relationship(back_populates="operator")
    outputs: Mapped[list["Output"]] = relationship(back_populates="operator")
    launches: Mapped[list["Launch"]] = relationship(back_populates="operator")


class Input(Base):
    __tablename__ = "inputs"
    __table_args__ = (UniqueConstraint("operator_id", "queue_id", name="uq_inputs"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    queue_id: Mapped[int] = mapped_column(ForeignKey("queues.id"), nullable=False)

    queue: Mapped["Queue"] = relationship(back_populates="inputs")
    operator: Mapped[Operator] = relationship(back_populates="inputs")


class Output(Base):
    __tablename__ = "outputs"
    __table_args__ = (UniqueConstraint("operator_id", "queue_id", name="uq_outputs"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    queue_id: Mapped[int] = mapped_column(ForeignKey("queues.id"), nullable=False)

    queue: Mapped["Queue"] = relationship(back_populates="outputs")
    operator: Mapped[Operator] = relationship(back_populates="outputs")


# Block jobs


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    saga_id: Mapped[int] = mapped_column(ForeignKey("sagas.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now(), onupdate=func.now())
    comment: Mapped[str] = mapped_column(TEXT(), nullable=True)
    status: Mapped[Status] = mapped_column(String(10), nullable=False, default=Status.PREPARING, index=True)

    saga: Mapped["Saga"] = relationship(back_populates="jobs")
    streams: Mapped[list["Stream"]] = relationship(back_populates="job")
    launches: Mapped[list["Launch"]] = relationship(back_populates="job")


class Stream(Base):
    __tablename__ = "streams"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    queue_id: Mapped[int] = mapped_column(ForeignKey("queues.id"), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False, index=True)

    job: Mapped["Job"] = relationship(back_populates="streams")
    queue: Mapped["Queue"] = relationship(back_populates="streams")
    values: Mapped[list["Value"]] = relationship(back_populates="stream")


class Value(Base):
    __tablename__ = "values"

    id: Mapped[int] = mapped_column(primary_key=True)
    stream_id: Mapped[int] = mapped_column(ForeignKey("streams.id"), nullable=False)
    launch_id: Mapped[int] = mapped_column(ForeignKey("launches.id"), nullable=False)
    data: Mapped[Any] = mapped_column(JSONB(), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False, index=True)

    stream: Mapped["Stream"] = relationship(back_populates="values")
    launch: Mapped["Launch"] = relationship(back_populates="values")


class Launch(Base):
    __tablename__ = "launches"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    status: Mapped[Status] = mapped_column(String(10), nullable=False, default=Status.PREPARING, index=True)

    job: Mapped["Job"] = relationship(back_populates="launches")
    operator: Mapped["Operator"] = relationship(back_populates="launches")
    values: Mapped[list["Value"]] = relationship(back_populates="launch")
