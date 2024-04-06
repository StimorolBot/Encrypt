import datetime
from uuid import UUID
from typing import TYPE_CHECKING, List

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model.declarative_base import Base

if TYPE_CHECKING:
    from src.app.auth.models.user import UserTable


class PathTable(Base):
    __tablename__ = "Path_Table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"))
    path: Mapped[str] = mapped_column(index=True, unique=True)
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="files")
    file_name: Mapped[List["FileTable"]] = relationship("FileTable", back_populates="path")


class FileTable(Base):
    __tablename__ = "File_Table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path_id: Mapped[int] = mapped_column(ForeignKey("File_Table.id"))
    file_name: Mapped[str] = mapped_column(index=True, unique=True)

    path: Mapped["PathTable"] = relationship("PathTable", back_populates="file_name")
