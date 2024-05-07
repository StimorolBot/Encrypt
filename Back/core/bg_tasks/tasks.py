import ssl
import smtplib
from email.message import EmailMessage
from core.bg_tasks.smtp_template import email_confirm
from core.bg_tasks.setting import smtp_setting, celery


@celery.task(name="send_email")
def send_email(ip_address: str, user_name: str, user_email=smtp_setting.ADMIN_EMAIL) -> str:
    email = EmailMessage()
    email["From"] = user_email
    email["To"] = smtp_setting.ADMIN_EMAIL
    context = ssl.create_default_context()

    msg, code = email_confirm(email=email, user_name=user_name, location=ip_address, user_email=user_email)

    with smtplib.SMTP_SSL(smtp_setting.host, smtp_setting.port, context=context) as server:
        server.login(smtp_setting.ADMIN_EMAIL, smtp_setting.PASSWORD)
        server.send_message(msg)

    return code
