from typing import List
from pydantic import Field
from pydantic import EmailStr, BaseModel
from core.validator.validator import BaseValidator


class FileName(BaseValidator):
    name: str = Field(..., min_length=4, max_length=30)


class PathDTO(BaseModel):
    file_name: List[FileName]


class FileDTO(BaseValidator):
    user_name: str
    email: EmailStr
    path: PathDTO


