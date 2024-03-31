from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict
from fastapi.param_functions import Form, Annotated
from pydantic.functional_validators import model_validator


class PasswordSchemas(BaseModel):
    password: Annotated[str, Form(min_length=4, max_length=24)]
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def password_len(self) -> str:
        password = self.password

        if (4 > len(password)) or (24 < len(password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Длинна пароля должна быть от 4 до 24 символов")

        return password


class FileSchemas(BaseModel):
    name: str
    size: int
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def file_size(self):
        size = self.size
        if size >= 10_000_000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Размер файла не должен превышать 10Мб")

    @model_validator(mode="after")
    def file_name(self):
        name = self.name
