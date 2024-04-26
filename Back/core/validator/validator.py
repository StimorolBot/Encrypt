import string
from fastapi import status, HTTPException
from pydantic import BaseModel, model_validator


def check_email(val: str):
    allowed_domains = ["gmail.com", "mail.ru"]
    alp = set(string.ascii_lowercase)
    name, domains = val.split("@")

    if domains not in allowed_domains:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неразрешенный домен почты")

    elif alp.isdisjoint(name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Почта не может содержать кириллицу")


def check_forbidden_symbols(val: str):
    symbols = {"[", "]", "\\", "^", "$", "|", "?", "*", "+", "(", ")", "{", "}", "/", "#", "'", '"', "@", " "}

    if symbols & set(val):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Поле не должно содержать: {symbols}")


def check_file_size(val: int):
    if val >= 10_000_000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Размер файла не должен превышать 10Мб")


func_valid_dict = {"email": check_email, "file_size": check_file_size,
                   "file_name": check_forbidden_symbols,
                   "user_name": check_forbidden_symbols,
                   "password": check_forbidden_symbols,
                   }


class BaseValidator(BaseModel):

    @model_validator(mode="after")
    @classmethod
    def test(cls, data):
        data_dict: dict = data.model_dump()
        for item in data_dict.items():
            func = func_valid_dict.get(item[0])
            if func:
                func(item[1])

        return data
