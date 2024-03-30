from fastapi import HTTPException, status
from fastapi.param_functions import Form, Annotated
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import model_validator


class CheckPassword(BaseModel):
    password: Annotated[str, Form(min_length=4, max_length=24)]
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def password_len(self):
        password = self.password

        if (4 > len(password)) or (24 < len(password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Длинна пароля должна быть от 4 до 24 символов")


class CheckFile(BaseModel):
    # file_name: str
    file_size: int
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def file_size(self):
        file_size = self.file_size

        if file_size >= 10_000_000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Размер файла не должен превышать 10Мб")
