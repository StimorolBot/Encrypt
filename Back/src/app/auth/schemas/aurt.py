from pydantic import BaseModel, EmailStr, ConfigDict


class RegisterSchemas(BaseModel):
    user_name: str
    password: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)
