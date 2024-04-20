from uuid import uuid4
from datetime import timedelta


def generate_uuid():
    return str(uuid4())


def get_seconds(day: int) -> int:
    return int(timedelta(days=day).total_seconds())
