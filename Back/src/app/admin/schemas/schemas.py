from enum import Enum
from pydantic import EmailStr
from core.validator.validator import BaseValidator


class DateType(Enum):
    seconds = "seconds"
    hours = "hours"
    days = "days"
    months = "months"
    years = "years"


class UserBlockUnlock(BaseValidator):
    email: EmailStr
    date_type: DateType
    date: int
