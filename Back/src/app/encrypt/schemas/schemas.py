from pydantic import BaseModel
from typing_extensions import Annotated
from fastapi.param_functions import Form


class FileSchemas(BaseModel):
    password: Annotated[str, Form(min_length=8, max_length=20)]
