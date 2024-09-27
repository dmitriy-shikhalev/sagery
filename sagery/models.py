import enum

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import String
from sqlalchemy import Index, Integer
from sqlalchemy.dialects.postgresql import ENUM, JSON
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


RequestItemTable = Table(
    'request_item',
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("request_id", Integer, ForeignKey("request.id")),
    Column("item_id", Integer, ForeignKey("item.id")),
)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"), nullable=False, index=True)
    job: Mapped["Job"] = relationship(back_populates="items")
    key: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(JSON(), nullable=False, default='null')

    __table_args__ = (
        Index("items_key", 'job_id', "key"),
    )


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    items: Mapped[list[Item]] = relationship(back_populates="job")
    requests: Mapped[list["Request"]] = relationship(back_populates="job")
    status: Status = Column(ENUM(Status), default=Status.PENDING, nullable=False)


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer(), init=False, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"), nullable=False, index=True)
    job: Mapped["Job"] = relationship(back_populates="requests")

    operator_name: Mapped[str] = Column(String(), nullable=False)
    status: Status = Column(ENUM(Status), default=Status.PENDING, nullable=False)
