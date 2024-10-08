import socket
from celery import Celery

from pydantic_settings import BaseSettings, SettingsConfigDict


class Smtp(BaseSettings):
    PASSWORD: str
    port: int = 465
    host: str = "smtp.gmail.com"
    ADMIN_EMAIL: str
    expire: int = 120
    worker_name: str = f"celery@{socket.gethostname()}"

    model_config = SettingsConfigDict(env_file="core/bg_tasks/.smtp.env")


smtp_setting = Smtp()

# http://localhost:5555/
# celery -A core.bg_tasks.setting:celery flower
# celery -A core.bg_tasks.setting:celery worker --loglevel=INFO --pool=solo
celery = Celery("smtp", broker="redis://localhost:6379", backend="redis://localhost:6379")
celery.autodiscover_tasks(["celery"])
