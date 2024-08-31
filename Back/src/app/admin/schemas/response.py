from uuid import UUID
from datetime import datetime

from pydantic import EmailStr, BaseModel


class UserResponseDTO(BaseModel):
    id: UUID
    user_name: str
    email: EmailStr
    date_register: datetime
    is_active: bool
    is_blocked: datetime | None
