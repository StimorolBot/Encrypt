from pydantic import BaseModel, EmailStr


class RegisterSchemas(BaseModel):
    user_name: str
    password: str
    email: EmailStr
