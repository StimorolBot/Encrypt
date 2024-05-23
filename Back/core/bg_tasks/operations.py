from pydantic import EmailStr
from email.message import EmailMessage
from fastapi import status, HTTPException
from src.app.auth.models.user import UserTable

from core.logger import user_logger
from core.operations.crud import Crud
from core.db import async_session_maker
from core.bg_tasks.smtp_template import email_confirm, reset_password


def generate_email(ip_address: str, type_email: str, user_agent: str, user_email: EmailStr, email: EmailMessage) -> list:
    match type_email:
        case "email_confirm":
            email_template, code_confirm = email_confirm(email=email, location=ip_address, user_email=user_email, user_agent=user_agent)
            user_logger.info(f"Запрос на создание аккаунта {user_email}")
        case "reset_password":
            email_template, code_confirm = reset_password(email=email, location=ip_address, user_email=user_email, user_agent=user_agent)
            user_logger.info(f"Запрос на сброс пароля {user_email}")
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидный тип письма")

    return [code_confirm, email_template]


async def unlock_user(email: EmailStr) -> dict:
    async with async_session_maker() as session:
        await Crud.update(
            session=session, table=UserTable,
            field=UserTable.email,
            field_val=email, data={"is_blocked": None}
        )
    user_logger.info(f"Пользователь {email} разблокирован в автоматическом режиме")
    return {"detail": f"Пользователь {email} разблокирован"}
