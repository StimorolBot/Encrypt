from pathlib import Path
from pydantic import BaseModel
from redis import asyncio as aioredis
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_path_key: Path = BASE_DIR / ".secret" / "jwt-private.pem"
    public_path_key: Path = BASE_DIR / ".secret" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30


class Setting(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    auth_jwt: AuthJWT = AuthJWT()

    BASE_PATH: str
    model_config = SettingsConfigDict(env_file="core/.env")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


setting = Setting()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
http_bearer = HTTPBearer(auto_error=False)
