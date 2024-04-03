from jose import jwt
from datetime import datetime, timedelta, timezone

from core.config import config, pwd_context
from fastapi.security import OAuth2PasswordRequestForm


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
