import jwt
from core.config import config
from datetime import datetime, timedelta, timezone


class JWTToken:
    @staticmethod
    async def encoded_jwt(payload: dict,
                          algorithm: str = config.auth_jwt.algorithm,
                          private_key: str = config.auth_jwt.private_path_key.read_text(),
                          expire_timedelta: timedelta | None = None,
                          expire_minutes: int = config.auth_jwt.access_token_expire_minutes):
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire, iat=now)
        return jwt.encode(to_encode, private_key, algorithm=algorithm)

    @staticmethod
    async def decoded_jwt(token: str,
                          algorithms: str = config.auth_jwt.algorithm,
                          public_key: str = config.auth_jwt.public_path_key.read_text()):
        return jwt.decode(token, public_key, algorithms=algorithms)

    @staticmethod
    async def create_token(token_type: str, token_data: dict, expire_timedelta: timedelta | None = None, ):
        jwt_payload = {"type": token_type}
        jwt_payload.update(token_data)
        return await JWTToken.encoded_jwt(payload=jwt_payload, expire_timedelta=expire_timedelta)
