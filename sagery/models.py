import enum

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Table
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import relationship


class Status(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    key: Mapped[str] = mapped_column(index=True)
    value: Mapped[str] = mapped_column()
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="datas")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    datas: Mapped[list[Data]] = relationship(back_populates="job")
    requests: Mapped[list["Request"]] = relationship(back_populates="job")
    status: Status = Column(Enum(Status), default=Status.PENDING, nullable=False)


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="requests")

    operator_name: Mapped[str] = Column(String(), nullable=False)
    status: Status = Column(Enum(Status), default=Status.PENDING, nullable=False)
