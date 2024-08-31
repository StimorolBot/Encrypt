import os
import string
import secrets
from time import time
from uuid import uuid4
from functools import wraps
from datetime import timedelta
from fastapi import Request, HTTPException, status


def generate_uuid():
    return str(uuid4())


def get_seconds(day: int) -> int:
    return int(timedelta(days=day).total_seconds())


def get_files(path: str) -> list:
    if os.path.exists(path) and os.path.isdir(path):
        return [f for f in os.listdir(path) if "." in f]  # доработать
    else:
        raise FileNotFoundError(f"[!] Директория '{path}' не найдена")


def generate_code(code_len: int = 6) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(secrets.choice(letters_and_digits) for _ in range(code_len))


def set_limited(max_calls: int, time_limit: int):
    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time()
            calls_limit = [call for call in calls if call > now - time_limit]
            if len(calls_limit) >= max_calls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Превышен лимит запросов")
            calls.append(now)
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
