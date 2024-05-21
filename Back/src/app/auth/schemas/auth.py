from uuid import UUID
from datetime import datetime
from core.validator.validator import BaseValidator
from pydantic import EmailStr, ConfigDict, Field


class BaseUser(BaseValidator):
    email: EmailStr = Field(..., min_length=8, max_length=30)


class UserCreate(BaseUser):
    user_name: str = Field(..., min_length=4, max_length=20)
    password: str = Field(..., min_length=4, max_length=24)
    code_confirm: str = Field(..., max_length=6, min_length=6)
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseUser):
    password: str = Field(..., min_length=4, max_length=24)


class UserRead(BaseUser):
    id: UUID
    user_name: str = Field(..., min_length=4, max_length=20)
    date_register: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResetPassword(BaseUser):
    code_confirm: str = Field(..., max_length=6, min_length=6)
    password: str = Field(..., min_length=4, max_length=24)

    model_config = ConfigDict(from_attributes=True)
