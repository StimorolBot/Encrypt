import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model.declarative_base import Base
from core.operations.operation import generate_uuid

if TYPE_CHECKING:
    from src.app.auth.models.user import UserTable


class FileTable(Base):
    __tablename__ = "File_Table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=generate_uuid)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"))
    path: Mapped[str] = mapped_column(index=True)
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="files")
