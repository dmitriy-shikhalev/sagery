from __future__ import annotations

from typing import TypeAlias

from sqlalchemy.ext.declarative import declarative_base


Base: TypeAlias = declarative_base()  # type: ignore


NAME_SIZE = 100
MAX_STRING_SIZE = 1024


from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import ARRAY, Column, Enum, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship

from tick.enums import Status
from tick.models.base import Base, MAX_STRING_SIZE
from tick.models.schema import Statement
from tick.models.schema import Schema, Thread


class Job(Base):
    __tablename__ = "job"

    id: Mapped[int] = Column(Integer, primary_key=True)
    schema_id: Mapped[int] = Column(ForeignKey("schema.id"))
    schema: Mapped[Schema] = relationship(Schema, backref="jobs")
    input_ids: Mapped[List[int]] = Column(ARRAY(Integer))
    inputs: Mapped[List['Row']] = relationship(
        'Row',
        primaryjoin='any_(Row.id == foreign(Job.input_ids))',
        uselist=True,
        remote_side='Row.id',
        viewonly=True,
    )
    # inputs: Mapped[List['Row']] = relationship(
    #     "Row",
    #     primaryjoin="and_(Job.id==Pride.job_id, Pride.type=='__enter__', Pride.id==Row.pride_id)",
    #     viewonly=True,
    #     uselist=True,
    # )
    output_ids: Mapped[List[int]] = Column(ARRAY(Integer), default=())
    outputs: Mapped[List['Row']] = relationship(
        'Row',
        primaryjoin='any_(Row.id == foreign(Job.input_ids))',
        uselist=True,
        remote_side='Row.id',
        viewonly=True,
    )
    # outputs: Mapped[List['Row']] = relationship(
    #     "Row",
    #     primaryjoin="and_(Job.id==Pride.job_id, Pride.type=='__exit__', Pride.id==Row.pride_id)",
    #     viewonly=True,
    #     uselist=True,
    # )
    status = Column(Enum(Status), default=Status.NEW)

    prides: Mapped[List[Pride]] = relationship(
        'Pride',
        back_populates="job", cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Job(id={self.id!r}, schema_id={self.schema_id!r}, inputs={self.inputs!r})"


class Pride(Base):
    __tablename__ = "pride"

    id: Mapped[int] = Column(Integer, primary_key=True)
    job_id: Mapped[int] = Column(ForeignKey('job.id'), nullable=False)
    job: Mapped[Job] = relationship(Job, back_populates="prides")
    thread_id: Mapped[int] = Column(ForeignKey("thread.id"), nullable=False)
    thread: Mapped[Thread] = relationship('Thread', backref="prides", lazy='joined')
    status = Column(Enum(Status), default=Status.NEW)

    requests: Mapped[List[Request]] = relationship('Request', back_populates='pride')
    publisher_binds: Mapped[List['Bind']] = relationship(
        'Bind',
        primaryjoin='all_(Bind.publisher_id == foreign(Pride.id))',
        uselist=True
    )
    subscriber_binds: Mapped[List['Bind']] = relationship(
        'Bind',
        primaryjoin='all_(Bind.subscriber_id == foreign(Pride.id))',
        uselist=True
    )

    def __repr__(self) -> str:
        return f"Pride(id={self.id!r}, job_id={self.job_id!r}, thread_id={self.thread_id!r}, " \
               f"status={self.status!r})"


class Request(Base):
    __tablename__ = "request"
    __table_args__ = (
        UniqueConstraint('pride_id', 'input_ids', name='unique_request_pride_id_inputs'),
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    request_id: Mapped[str] = Column(String(MAX_STRING_SIZE), nullable=True)
    pride_id: Mapped[int] = Column(ForeignKey('pride.id'), nullable=False)
    pride: Mapped[Pride] = relationship('Pride', back_populates="requests")
    input_ids: Mapped[List[int]] = Column(ARRAY(Integer))
    inputs: Mapped[List['Row']] = relationship(
        'Row',
        primaryjoin='any_(Row.id == foreign(Request.input_ids))',
        uselist=True
    )
    output_ids: Mapped[List[int]] = Column(ARRAY(Integer), default=())
    outputs: Mapped[List['Row']] = relationship(
        'Row',
        primaryjoin='any_(Row.id == foreign(Request.output_ids))',
        uselist=True
    )
    status: Mapped[Status] = Column(Enum(Status), default=Status.NEW)

    def __repr__(self) -> str:
        return f"Request(id={self.id!r}, pride_id={self.pride_id!r}, status={self.status!r})"


class Bind(Base):
    __tablename__ = 'bind'
    __table_args__ = (
        UniqueConstraint('publisher_id', 'subscriber_id', name='unique_publisher_subscriber_bind'),
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    publisher_id: Mapped[int] = Column(ForeignKey('pride.id'), nullable=True)
    publisher: Mapped[Pride] = relationship(
        'Pride',
        back_populates="publisher_binds",
        primaryjoin='Bind.publisher_id == foreign(Pride.id)',
    )
    subscriber_id: Mapped[int] = Column(ForeignKey('pride.id'), nullable=False)
    subscriber: Mapped[Pride] = relationship(
        'Pride',
        back_populates="subscriber_binds",
        primaryjoin='Bind.subscriber_id == foreign(Pride.id)',
    )
