import pytest
from core.operations.crud import Crud
from tests.conftest import async_session_maker
from src.app.auth.models.user import UserTable
from src.app.encrypt.models.model import PathTable


@pytest.fixture(autouse=True, scope="session")
async def add_record():
    async with async_session_maker() as session:
        await Crud.create(session=session, table=UserTable,
                          data_dict={"email": "test@gmail.com", "user_name": "username", "password": "password"})
        await Crud.create(session=session, table=PathTable,
                          data_dict={"email": "test@gmail.com", "path": ".test_file/test@gmail.com"})
