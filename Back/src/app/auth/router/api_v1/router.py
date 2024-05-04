from datetime import timedelta
from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.app.auth.token import JWTToken
from src.app.auth.token_type import TokenType
from src.app.auth.models.user import UserTable
from src.app.auth.user_manager import UserManager
from src.app.auth.schemas.token import TokenSchemas
from src.app.auth.schemas.auth import UserCreate, UserRead

from core.setting import setting
from core.logger import user_logger
from core.operations.crud import Crud
from core.db import get_async_session
from core.bg_tasks.smtp import send_email
from core.operations.operation import get_seconds

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(tags=["auth"], prefix="/auth")


@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_schemas: UserCreate, session: "AsyncSession" = Depends(get_async_session)):
    user = await Crud.read(table=UserTable, session=session, field=UserTable.email, value=user_schemas.email)

    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с такой почтой уже существует")

    user_dict = await UserManager.config_user(user_dict=user_schemas.model_dump())
    create_user = await Crud.create(data_dict=user_dict, session=session, table=UserTable)
    user_logger.info(f"Пользователь {user_schemas.email} создал аккаунт")

    return create_user


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchemas, response_model_exclude_none=True)
async def login_user(response: Response, user: UserRead = Depends(UserManager().check_user)):
    access_token = await JWTToken.create_token(token_type=TokenType.ACCESS.value,
                                               token_data={"sub": str(user.id), "email": user.email})

    refresh_token = await JWTToken.create_token(token_type=TokenType.REFRESH.value, token_data={"sub": str(user.id)},
                                                expire_timedelta=timedelta(days=setting.auth_jwt.refresh_token_expire_days))

    exp = get_seconds(setting.auth_jwt.refresh_token_expire_days)
    # не устанавливаются
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=exp, expires=exp, httponly=True, domain="127.0.0.1", samesite="none")
    user_logger.info(f"Пользователь {user.email} вошел в систему")
    return TokenSchemas(access_token=access_token, refresh_token=refresh_token, refresh_max_age=exp)


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response, session: "AsyncSession" = Depends(get_async_session),
                      current_user: "UserRead" = Depends(UserManager.get_current_user)):
    response.delete_cookie(key="refresh_token")
    await Crud.update(session=session, table=UserTable, field=UserTable.email, field_val=current_user.email, data={"is_active": False})


@auth_router.post("/refresh", response_model=TokenSchemas, response_model_exclude_none=True)
async def refresh_jwt_token(token=Depends(UserManager.get_current_user_for_refresh_token)):
    return TokenSchemas(access_token=token)


@auth_router.get("/email-confirm")
async def email_confirm():
    send_email.delay("Sling Academy")


@auth_router.post("/reset-password")
async def reset_password():
    return "Сброс пароля!"
