from jose import jwt
from typing import TYPE_CHECKING
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.auth.models.user import UserTable

from core.operations.crud import Crud
from core.db import get_async_session
from core.config import config, pwd_context, cookie_scheme

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserManager:
    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def check_user(self, user: OAuth2PasswordRequestForm, password: str) -> bool:
        if user is None:
            return False
        else:
            await self.verify_password(password, user.password)

    @staticmethod
    async def config_user(user_dict: dict) -> dict:
        user_dict["password"] = pwd_context.hash(user_dict["password"])
        user_dict["is_active"] = False
        user_dict["is_superuser"] = False
        user_dict["is_verified"] = False

        return user_dict

    @staticmethod
    async def get_current_user(session: "AsyncSession" = Depends(get_async_session), cookie_session: str = Depends(cookie_scheme)) -> dict:
        decode_jwt = jwt.decode(key=config.SECRET_KEY, token=cookie_session)
        current_user = await Crud.read_one(session=session, table=UserTable, field=UserTable.email, value=decode_jwt["email"])
        return current_user.__dict__
