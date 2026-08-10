from sqlalchemy import CHAR, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sagery.db.base import Base


# Block Schema


class Saga(Base):
    __tablename__ = "sagas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(CHAR(50), nullable=True, index=True)
    comment: Mapped[str] = mapped_column(TEXT(), nullable=True)
    queues: Mapped[list["Queue"]] = relationship(back_populates="saga")


class Queue(Base):
    __tablename__ = "queues"

    id: Mapped[int] = mapped_column(primary_key=True)
    saga_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(CHAR(50), nullable=False, index=True)
    saga: Mapped["Saga"] = relationship(back_populates="queues")


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(CHAR(50), nullable=False, index=True)
    args_mapper: Mapped[dict[str, str]] = mapped_column(JSONB(), nullable=False, server_default="{}")


# Block jobs


