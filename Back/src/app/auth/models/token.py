from typing import TYPE_CHECKING

from core.model.declarative_base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.app.auth.models.user import UserTable


class TokenTable(Base):
    __tablename__ = "Token_Table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(ForeignKey("User_Table.email"), index=True, unique=True)
    refresh_token: Mapped[str | None] = mapped_column(unique=True)

    user_token: Mapped["UserTable"] = relationship(back_populates="refresh_token")
