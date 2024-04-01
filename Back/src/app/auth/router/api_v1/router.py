from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends

from core.operations.crud import Crud
from core.db import get_async_session
from src.app.auth.models.user import UserTable
from src.app.auth.schemas.aurt import RegisterSchemas

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/register")
async def register_user(user_create: RegisterSchemas = Depends(), session: "AsyncSession" = Depends(get_async_session)):
    await Crud.create(data_dict=user_create.model_dump(), session=session, table=UserTable)
