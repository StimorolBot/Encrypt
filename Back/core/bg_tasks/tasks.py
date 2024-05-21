import ssl
import smtplib
from pydantic import EmailStr
from email.message import EmailMessage
from fastapi import status, HTTPException

from core.logger import user_logger
from core.bg_tasks.setting import smtp_setting, celery
from core.bg_tasks.smtp_template import email_confirm, reset_password


@celery.task(name="send_email", max_retries=3, default_retry_delay=30)
def send_email(ip_address: str, type_email: str, user_agent: str, user_email: EmailStr = smtp_setting.ADMIN_EMAIL) -> str:
    email = EmailMessage()
    email["From"] = user_email
    email["To"] = smtp_setting.ADMIN_EMAIL
    context = ssl.create_default_context()

    match type_email:
        case "email_confirm":
            email_template, code_confirm = email_confirm(email=email, location=ip_address, user_email=user_email, user_agent=user_agent)
            user_logger.info(f"Запрос на создание аккаунта {user_email}")
        case "reset_password":
            email_template, code_confirm = reset_password(email=email, location=ip_address, user_email=user_email, user_agent=user_agent)
            user_logger.info(f"Запрос на сброс пароля {user_email}")
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидный тип письма")

    with smtplib.SMTP_SSL(smtp_setting.host, smtp_setting.port, context=context) as server:
        server.login(smtp_setting.ADMIN_EMAIL, smtp_setting.PASSWORD)
        server.send_message(email_template)

    return code_confirm
