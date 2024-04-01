import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from core.model.declarative_base import Base
from core.operations.operation import generate_uuid


class UserTable(Base):
    __tablename__ = "User_Table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=generate_uuid)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    date_register: Mapped[datetime.datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
