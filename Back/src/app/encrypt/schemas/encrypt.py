from pydantic import ConfigDict, Field
from core.validator.validator import BaseValidator


class EncryptSchemas(BaseValidator):
    file_name: str = Field(..., min_length=4, max_length=30)
    file_size: int
    password: str = Field(..., min_length=4, max_length=24)

    model_config = ConfigDict(from_attributes=True)
