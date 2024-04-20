from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class BaseUser(BaseModel):
    email: EmailStr


class UserCreate(BaseUser):
    user_name: str
    password: str
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseUser):
    password: str


class UserRead(BaseUser):
    id: UUID
    user_name: str
    date_register: datetime

    model_config = ConfigDict(from_attributes=True)
