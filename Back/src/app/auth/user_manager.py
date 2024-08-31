from jwt.exceptions import DecodeError
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status, Header, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from src.app.auth.token import JWTToken
from src.app.auth.token_type import TokenType
from src.app.auth.models.user import UserTable
from src.app.auth.schemas.auth import UserRead, UserLogin

from core.operations.crud import Crud
from core.db import get_async_session
from core.setting import pwd_context

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserManager:
    @classmethod
    async def verify_password(cls, user: OAuth2PasswordRequestForm, password: str) -> bool:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин/пароль")
        else:
            return pwd_context.verify(password, user.password)

    async def check_user(self, data_login: UserLogin, session: "AsyncSession" = Depends(get_async_session)):
        user = await Crud.read(session=session, table=UserTable, field=UserTable.email, value=data_login.email)
        if await self.verify_password(user=user, password=data_login.password) is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин/пароль")
        return user

    @staticmethod
    async def config_user(user_dict: dict) -> dict:

        user_dict["password"] = pwd_context.hash(user_dict["password"])
        del user_dict["code_confirm"]
        user_dict["is_active"] = False
        user_dict["is_superuser"] = False  # удалить
        user_dict["is_verified"] = False

        return user_dict

    @staticmethod
    async def get_current_user_for_refresh_token(refresh_token: str | None = Cookie(default=None),
                                                 session: "AsyncSession" = Depends(get_async_session)):
        payload = await JWTToken.validate_token_type(token=refresh_token, token_type=TokenType.REFRESH.value)
        current_user: UserRead = await Crud.read(table=UserTable, session=session, field=UserTable.email, value=payload["sub"])
        access_token = await JWTToken.create_token(token_type=TokenType.ACCESS.value,
                                                   token_data={"sub": current_user.email, "email": current_user.email})
        return access_token

    @staticmethod
    async def get_current_user(access_token: Annotated[str | None, Header(alias="Authorization")] = None,
                               session: "AsyncSession" = Depends(get_async_session)) -> UserRead:
        try:
            payload = await JWTToken.validate_token_type(token=access_token.split("Bearer ")[1], token_type=TokenType.ACCESS.value)
            current_user: UserRead = await Crud.read(table=UserTable, session=session, field=UserTable.email, value=payload["email"])
            return current_user

        except (IndexError, AttributeError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неуказан тип токена")

        except DecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат токена")
