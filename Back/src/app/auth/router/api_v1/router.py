from datetime import timedelta
from typing import TYPE_CHECKING, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.app.auth.models.user import UserTable
from src.app.auth.user_manager import UserManager
from src.app.auth.schemas.aurt import RegisterSchemas

from core.config import config
from core.operations.crud import Crud
from core.db import get_async_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/register", response_model=RegisterSchemas, status_code=status.HTTP_201_CREATED)
async def register_user(user_schemas: Annotated[RegisterSchemas, Depends()], session: "AsyncSession" = Depends(get_async_session)):
    user = await Crud.read_one(table=UserTable, session=session, field=UserTable.email, value=user_schemas.email)

    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с такой почтой уже существует")
    user_dict = await UserManager.config_user(user_dict=user_schemas.model_dump())
    create_user = await Crud.create(data_dict=user_dict, session=session, table=UserTable)

    return create_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(response: Response, user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     session: "AsyncSession" = Depends(get_async_session)):  # в OAuth2PasswordRequestForm нет поля email
    user = await Crud.read_one(session=session, table=UserTable, field=UserTable.email, value=user_data.username)

    if await UserManager().check_user(user=user, password=user_data.password) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный логин/пароль")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await UserManager.create_access_token(data={"email": user.email}, expires_delta=access_token_expires)
    return response.set_cookie(key="access_token", value=access_token)


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return "OK"


@auth_router.post("/texx")
async def test(s=Depends(UserManager.get_current_user)):
    print(s)
    return s
