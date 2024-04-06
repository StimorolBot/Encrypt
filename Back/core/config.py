from redis import asyncio as aioredis
from passlib.context import CryptContext
from fastapi.security import APIKeyCookie
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    BASE_PATH: str
    model_config = SettingsConfigDict(env_file="core/.env")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()
template = Jinja2Templates(directory="../Front/")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cookie_scheme = APIKeyCookie(name="access_token")
redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
