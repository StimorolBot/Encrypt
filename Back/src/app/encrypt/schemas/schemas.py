from typing_extensions import Annotated
from fastapi.param_functions import Form
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import model_validator


class CheckPassword(BaseModel):
    password: Annotated[str, Form(min_length=8, max_length=20)]
    model_config = ConfigDict(from_attributes=True)


class CheckFeli(BaseModel):
    file_name: str
    file_size: int
    model_config = ConfigDict(from_attributes=True)
