from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.operations.crud import Crud
from core.db import get_async_session
from core.bg_tasks.setting import celery
from core.logger import user_logger, os_logger
from core.bg_tasks.setting import smtp_setting
from core.bg_tasks.tasks import unlock_user_task

from src.app.admin.operations import get_date
from src.app.auth.models.user import UserTable
from src.app.admin.schemas.schemas import UserBlockUnlock
from src.app.admin.schemas.response import UserResponseDTO

admin_router = APIRouter(tags=["admin"], prefix="/admin")


# добавить проверку на администратора
@admin_router.get("/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    all_user = await Crud.read_all(session=session, table=UserTable)
    return [UserResponseDTO.model_validate(item, from_attributes=True) for item in all_user]


@admin_router.get("/all-user-info")
async def get_all_user_info(session: AsyncSession = Depends(get_async_session)):
    return "work"


@admin_router.patch("/block", status_code=status.HTTP_200_OK)
async def block_user(user_data: UserBlockUnlock, session: "AsyncSession" = Depends(get_async_session)) -> dict:
    date = await get_date(date=user_data.date, type_date=user_data.date_type.value)

    await Crud.update(
        session=session, table=UserTable, field=UserTable.email,
        field_val=user_data.email, data={"is_blocked": date}
    )
    unlock_user_task.apply_async(kwargs={"email": user_data.email}, eta=date)

    user_logger.info(f"Пользователь {user_data.email} заблокирован до {date}")
    return {"detail": f"Пользователь {user_data.email} заблокирован до {date}"}


@admin_router.patch("/unlock", status_code=status.HTTP_200_OK)
async def unlock_user(email: str, session: "AsyncSession" = Depends(get_async_session)) -> dict:
    scheduled_task = celery.control.inspect().scheduled()
    tasks_info = scheduled_task[smtp_setting.worker_name]
    task_id = [task["request"]["id"] for task in tasks_info if task["request"]["kwargs"].get("email") == email]

    if task_id:
        os_logger.info(f"Задача {task_id[0]} удалена")
        celery.control.revoke(task_id[0], terminate=True)

    await Crud.update(
        session=session, table=UserTable,
        field=UserTable.email,
        field_val=email, data={"is_blocked": None}
    )

    user_logger.info(f"Пользователь {email} разблокирован в ручном режиме")
    return {"detail": f"Пользователь {email} разблокирован в ручном режиме"}


@admin_router.delete("/delete")
async def delete_user(email: str, session: "AsyncSession" = Depends(get_async_session)) -> dict:
    await Crud.delete(session=session, table=UserTable, field=UserTable.email, field_val=email)
    user_logger.info(f"Пользователь {email} удален")
    return {"detail": f"Пользователь {email} удален"}


@admin_router.patch("/black-list")
async def add_token_black_list(user_id: str, session: "AsyncSession" = Depends(get_async_session)) -> dict:
    return {"detail": f"Токен в черном списке {user_id}"}
