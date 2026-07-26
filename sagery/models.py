from sqlalchemy import CHAR, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from sagery.db.base import Base


class Saga(Base):
    __tablename__ = "sagas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(CHAR(50), nullable=True, index=True)
    comments: Mapped[str] = mapped_column(TEXT(1024), nullable=True)