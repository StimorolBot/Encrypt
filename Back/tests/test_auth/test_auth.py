import pytest
from fastapi import status
from tests.conftest import ac
from core.setting import redis
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient


# pytest  -vv -s  tests/test_auth/test_auth.py::TestAuthPos - запуск тестов
class TestAuthPos:
    async def test_email_confirm(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@gmail.com"}
        response = await ac.post("/auth/email-confirm", json=user_data)
        assert response.status_code == status.HTTP_200_OK

    async def test_register(self, ac: "AsyncClient"):
        code_confirm = await redis.get(name="test_11_22@gmail.com")
        user_data = {
            "email": "test_11_22@gmail.com", "user_name": "nametest",
            "password": "passwordtest", "code_confirm": code_confirm
        }
        response = await ac.post("/auth/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_login(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@gmail.com", "password": "passwordtest"}
        response = await ac.post("/auth/login", json=user_data)

        response_data = response.json()
        await redis.set(name="test_access_token", value=response_data["access_token"], ex=20)

        assert response.status_code == status.HTTP_200_OK

    async def test_logout(self, ac: "AsyncClient"):
        access_token = await redis.get(name="test_access_token")
        response = await ac.post("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == status.HTTP_200_OK


class TestAuthNeg:
    @pytest.mark.parametrize("email", [" ", "Email", "email@", " email @gmail.com", "email@test.com", "почта@mail.ru"])
    async def test_email(self, ac: "AsyncClient", email):
        user_data = {"email": email, "user_name": "nametest", "password": "passwordtest", "code_confirm": "code_confirm"}
        response = await ac.post("/auth/register", json=user_data)

        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("user_name, email", [
        (" ", "test_1_1@gmail.com"),
        ("UserNameUserNameUserNameUserNameUserNameUserName", "test_2_2@gmail.com"),
        ("Usr", "test_2_2@gmail.com"),
        ("user_name@", "test_3_3@gmail.com"),
        ("username username", "test_4_4@gmail.com")
    ])
    async def test_username_password(self, ac: "AsyncClient", user_name, email):
        user_data = {"email": email, "user_name": user_name, "password": "passwordtest", "code_confirm": "code_confirm"}
        response = await ac.post("/auth/register", json=user_data)

        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("code_confirm", [" ", "test code", "AASSDD", "123456", " 1 2 3", "привет", "Code12"])
    async def test_code_confirm(self, ac: "AsyncClient", code_confirm: str):
        user_data = {
            "email": "test_11_22@gmail.com", "user_name": "nametest", "password": "passwordtest",
            "code_confirm": code_confirm
        }
        response = await ac.post("/auth/register", json=user_data)

        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            assert response.status_code == status.HTTP_400_BAD_REQUEST
