import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model.declarative_base import Base

if TYPE_CHECKING:
    from src.app.auth.models.user import UserTable


class PathTable(Base):
    __tablename__ = "Path_Table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(ForeignKey("User_Table.email"), index=True, unique=True)
    path: Mapped[str] = mapped_column(unique=True)
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="path")
    file_name: Mapped[List["FileTable"]] = relationship(back_populates="path")


class FileTable(Base):
    __tablename__ = "File_Table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(ForeignKey("Path_Table.email"))
    name: Mapped[str] = mapped_column(index=True, unique=True)

    path: Mapped["PathTable"] = relationship(back_populates="file_name")
