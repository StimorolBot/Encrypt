from fastapi.param_functions import Form
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator


class PasswordSchemas(BaseModel):
    password: str = Form(min_length=4, max_length=24)
    model_config = ConfigDict(from_attributes=True)

    @field_validator("password")
    @classmethod
    def password_len(cls, password) -> str:
        if (4 > len(password)) or (24 < len(password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Длинна пароля должна быть от 4 до 24 символов")

        return password


class FileSchemas(BaseModel):
    name: str
    size: int
    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    @classmethod
    def file_name(cls, name):
        symbols = {"[", "]", "\\", "^", "$", "|", "?", "*", "+", "(", ")", "{", "}", "/", "#", "'", '"', "@"}

        if symbols & set(name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Имя файла не должно содержать: {symbols}")

    @field_validator("size")
    @classmethod
    def file_size(cls, size):
        if size >= 10_000_000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Размер файла не должен превышать 10Мб")
