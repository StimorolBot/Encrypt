import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model.declarative_base import Base
from core.operations.operation import generate_uuid

if TYPE_CHECKING:
    from src.app.encrypt.models.model import PathTable


class UserTable(Base):
    __tablename__ = "User_Table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=generate_uuid, index=True)
    user_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    refresh_token: Mapped[str | None] = mapped_column()
    date_register: Mapped[datetime.datetime] = mapped_column(server_default=func.CURRENT_TIMESTAMP())
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    path: Mapped["PathTable"] = relationship(back_populates="user")
