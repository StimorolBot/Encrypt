from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator


class EncryptSchemas(BaseModel):
    file_name: str
    file_size: int
    password: str
    model_config = ConfigDict(from_attributes=True)

    @field_validator("file_name")
    @classmethod
    def file_name(cls, file_name):
        symbols = {"[", "]", "\\", "^", "$", "|", "?", "*", "+", "(", ")", "{", "}", "/", "#", "'", '"', "@"}

        if symbols & set(file_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Имя файла не должно содержать: {symbols}")

    @field_validator("file_size")
    @classmethod
    def file_size(cls, file_size):
        if file_size >= 10_000_000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Размер файла не должен превышать 10Мб")

    @field_validator("password")
    @classmethod
    def password_len(cls, password):
        if (4 > len(password)) or (24 < len(password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Длинна пароля должна быть от 4 до 24 символов")
