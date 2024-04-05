from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class BaseUser(BaseModel):
    user_name: str
    email: EmailStr
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseUser):
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseUser):
    id: UUID
    date_register: datetime

    model_config = ConfigDict(from_attributes=True)
