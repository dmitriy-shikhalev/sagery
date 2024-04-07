from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import relationship

from .status import JobStatus, RequestStatus


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


saga_operator_table = Table(
    "saga_operator_table",
    Base.metadata,
    Column("saga_name", ForeignKey("saga.name"), primary_key=True),
    Column("operator_name", ForeignKey("operator.name"), primary_key=True),
)


class Saga(Base):
    __tablename__ = "saga"

    name: Mapped[str] = mapped_column(init=False, primary_key=True)
    operators: Mapped[list["Operator"]] = relationship(
        secondary=saga_operator_table, back_populates="sagas"
    )


class Operator(Base):
    __tablename__ = "operator"

    name: Mapped[str] = mapped_column(init=False, primary_key=True)
    sagas: Mapped[list[Saga]] = relationship(
        secondary=saga_operator_table, back_populates="operators"
    )
    requests: Mapped[list["Request"]] = relationship(back_populates="operator")


class Data(Base):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    key: Mapped[str] = mapped_column(init=False)
    value: Mapped[str] = mapped_column(init=False)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="datas")


class Job(Base):
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    datas: Mapped[list[Data]] = relationship(back_populates="job")
    requests: Mapped[list["Request"]] = relationship(back_populates="job")
    status: JobStatus = Column(Enum(JobStatus), default=JobStatus.PENDING)


class JobOperatorData(Base):
    __tablename__ = "job_operator_data"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped[Job] = relationship(back_populates="job_operator_datas")
    operator_name: Mapped[int] = mapped_column(ForeignKey("operator.name"))
    operator: Mapped[Operator] = relationship(back_populates="job_operator_datas")
    data_id: Mapped[int] = mapped_column(ForeignKey("data.id"))
    data: Mapped[Data] = relationship(back_populates="job_operator_datas")


class Request(Base):
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="requests")
    external_id: Mapped[str] = mapped_column(init=False, nullable=True, default=None)
    operator_name: Mapped[int] = mapped_column(ForeignKey("operator.name"))
    operator: Mapped["Operator"] = relationship(back_populates="requests")
    inputs: Mapped[list["Input"]] = relationship(back_populates="request")
    outputs: Mapped[list["Output"]] = relationship(back_populates="request")
    status: RequestStatus = Column(Enum(RequestStatus), default=RequestStatus.PENDING)


class Input(Base):
    __tablename__ = "input"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(init=False)
    request_id: Mapped[int] = mapped_column(ForeignKey("request.id"))
    request: Mapped[Request] = relationship(back_populates="inputs")


class Output(Base):
    __tablename__ = "output"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(init=False)
    request_id: Mapped[int] = mapped_column(ForeignKey("request.id"))
    request: Mapped[Request] = relationship(back_populates="outputs")
