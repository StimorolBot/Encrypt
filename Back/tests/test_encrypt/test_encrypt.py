import pytest
from tests.config import config_test
from tests.conftest import async_session_maker
from src.app.encrypt.operations import encrypt
from core.operations.operation import get_files

#  pytest  -vv -s  tests/test_encrypt/test_encrypt.py

file_list = get_files(f"{config_test.BASE_TEST_PATH}/test@gmail.com")


@pytest.mark.parametrize("file", file_list)
async def test_encrypt_pos(file: str):
    async with async_session_maker() as session:
        result = await encrypt(dir_="test@gmail.com", file_name=file, base_path=config_test.BASE_TEST_PATH,
                               password="test_password", session=session)

        assert type(result) is list
