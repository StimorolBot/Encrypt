import jwt
from core.setting import setting
from fastapi import status, HTTPException
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError


class JWTToken:
    @staticmethod
    async def encoded_jwt(payload: dict,
                          algorithm: str = setting.auth_jwt.algorithm,
                          private_key: str = setting.auth_jwt.private_path_key.read_text(),
                          expire_timedelta: timedelta | None = None,
                          expire_minutes: int = setting.auth_jwt.access_token_expire_minutes):
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
                          algorithms: str = setting.auth_jwt.algorithm,
                          public_key: str = setting.auth_jwt.public_path_key.read_text()):
        return jwt.decode(token, public_key, algorithms=algorithms)

    @staticmethod
    async def create_token(token_type: str, token_data: dict, expire_timedelta: timedelta | None = None, ):
        jwt_payload = {"type": token_type}
        jwt_payload.update(token_data)
        return await JWTToken.encoded_jwt(payload=jwt_payload, expire_timedelta=expire_timedelta)

    @staticmethod
    async def validate_token_type(token: str, token_type) -> dict:
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")

        try:
            payload = await JWTToken.decoded_jwt(token)
            if payload.get("type") != token_type:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный тип токена")
            return payload

        except InvalidSignatureError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидный токен")

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Время жизни токена истекло")
