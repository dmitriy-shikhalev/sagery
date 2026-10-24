from datetime import datetime
from typing import Any

from sqlalchemy import TEXT, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sagery.db import Base
from sagery.enums import Status, StreamStatus


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    saga_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now(), onupdate=func.now())
    comment: Mapped[str] = mapped_column(TEXT(), nullable=True)
    status: Mapped[Status] = mapped_column(String(10), nullable=False, default=Status.PREPARING, index=True)

    streams: Mapped[list["Stream"]] = relationship(back_populates="job")
    launches: Mapped[list["Launch"]] = relationship(back_populates="job")


class Stream(Base):
    __tablename__ = "streams"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    queue_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[StreamStatus] = mapped_column(String(10), nullable=False, default=StreamStatus.NEW, index=True)

    job: Mapped["Job"] = relationship(back_populates="streams")
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
    operator_name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[dict] = mapped_column(JSONB(), nullable=True)
    status: Mapped[Status] = mapped_column(String(10), nullable=False, default=Status.PREPARING, index=True)

    job: Mapped["Job"] = relationship(back_populates="launches")
    values: Mapped[list["Value"]] = relationship(back_populates="launch")
