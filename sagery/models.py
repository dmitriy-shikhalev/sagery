from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship

from sagery.enums import Status, ThreadStatus


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses."""


class Item(Base):
    """Class for representing an item in the sagery database."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"), nullable=False, index=True)
    object: Mapped["Object"] = relationship(back_populates="items", passive_deletes=True)
    key: Mapped[str] = mapped_column(String(), nullable=False, index=True)
    value: Mapped[str] = mapped_column(String(), nullable=True)


class Object(Base):
    """Class for representing an object in the sagery database."""

    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    thread: Mapped["Thread"] = relationship(back_populates="objects", passive_deletes=True)
    index: Mapped[int] = mapped_column(Integer(), nullable=False)

    items: Mapped[list[Item]] = relationship(
        Item,
        back_populates="object",
    )
    request: Mapped["Request"] = relationship("Request", back_populates="object")

    __table_args__ = (Index("uix_objects", "thread_id", "index", unique=True),)


class FunctionCall(Base):
    """Function launch."""

    __tablename__ = "function_calls"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    job: Mapped["Job"] = relationship(back_populates="function_calls", passive_deletes=True)
    pos: Mapped[int] = mapped_column(Integer(), nullable=False)
    index: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    status: Mapped[Status] = mapped_column(ENUM(Status), default=Status.PENDING, nullable=False, index=True)

    __table_args__ = (Index("uix_job_function_call", "job_id", "pos", unique=True),)


class Thread(Base):
    """Class for representing a thread in the sagery database."""

    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    job: Mapped["Job"] = relationship(back_populates="threads", passive_deletes=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)

    objects: Mapped[list[Object]] = relationship(Object, back_populates="thread")

    status: Mapped[ThreadStatus] = mapped_column(
        ENUM(ThreadStatus), default=ThreadStatus.OPEN, nullable=False, index=True
    )

    __table_args__ = (Index("uix_job_thread", "job_id", "name", unique=True),)


class Request(Base):
    """Class for representing a request in the sagery database."""

    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"), nullable=False, unique=True)
    object: Mapped["Object"] = relationship(back_populates="request", passive_deletes=True)

    operator_name: Mapped[str] = mapped_column(String(), nullable=False, index=True)
    status: Mapped[Status] = mapped_column(ENUM(Status), default=Status.PENDING, nullable=False, index=True)


class Job(Base):
    """Class for representing a job in the sagery database."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False, index=True)
    threads: Mapped[list[Thread]] = relationship(back_populates="job")
    function_calls: Mapped[list[FunctionCall]] = relationship(back_populates="job")
    status: Mapped[Status] = mapped_column(ENUM(Status), default=Status.PENDING, nullable=False, index=True)
