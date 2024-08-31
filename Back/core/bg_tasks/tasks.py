import ssl
import smtplib
import asyncio
from pydantic import EmailStr
from email.message import EmailMessage

from core.bg_tasks.setting import smtp_setting, celery
from core.bg_tasks.operations import generate_email, unlock_user


@celery.task(name="send_email", max_retries=3, default_retry_delay=3, limit=3)
def send_email(ip_address: str, type_email: str, user_agent: str, user_email: EmailStr = smtp_setting.ADMIN_EMAIL) -> str:
    email = EmailMessage()
    email["From"] = user_email
    email["To"] = smtp_setting.ADMIN_EMAIL
    context = ssl.create_default_context()

    code_confirm, email_template = generate_email(
        ip_address=ip_address, type_email=type_email,
        user_agent=user_agent, user_email=user_email, email=email
    )

    with smtplib.SMTP_SSL(smtp_setting.host, smtp_setting.port, context=context) as server:
        server.login(smtp_setting.ADMIN_EMAIL, smtp_setting.PASSWORD)
        server.send_message(email_template)

    return code_confirm


@celery.task(name="unlock_user", max_retries=3, default_retry_delay=10)
def unlock_user_task(**kwargs):
    asyncio.run(unlock_user(kwargs["email"]))
