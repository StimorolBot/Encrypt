from tests.conftest import ac
from typing import TYPE_CHECKING
from fastapi import status

if TYPE_CHECKING:
    from httpx import AsyncClient


# pytest  -vv -s  tests/test_auth.py::TestAuth - запуск тестов
class TestAuthPos:
    async def test_register(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com", "user_name": "nametest", "password": "passwordtest"}
        response = await ac.post("/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_login(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com", "password": "passwordtest"}
        response = await ac.post("/login", json=user_data)
        assert response.status_code == status.HTTP_200_OK

    async def test_logout(self, ac: "AsyncClient"):
        response = await ac.post("/logout")
        assert response.status_code == status.HTTP_200_OK


class TestAuthNeg:
    async def test_register(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com", "user_name": "nametest", "password": "passwordtest"}
        response = await ac.post("/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_login(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com", "password": "passwordtest-123"}
        response = await ac.post("/login", json=user_data)
        assert response.status_code == status.HTTP_200_OK

