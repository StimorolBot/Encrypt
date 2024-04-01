import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from core.model.declarative_base import Base
from core.operations.operation import generate_uuid


class FileTable(Base):
    __tablename__ = "File_Table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=generate_uuid)
    path: Mapped[str] = mapped_column()
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
