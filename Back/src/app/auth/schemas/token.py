from pydantic import BaseModel


class TokenSchemas(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    refresh_max_age: int | None = None
