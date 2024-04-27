import pytest
from fastapi import status, HTTPException
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


@pytest.mark.parametrize("file, path, password, exp", [
    (" ", " ", "test_password", pytest.raises(HTTPException)),
    ("non_existent.txt", "non_existent_path", "test_password", pytest.raises(HTTPException)),
    ("test.png.aes", ".test_file/test@gmail.com", "password", pytest.raises(HTTPException))
])
async def test_encrypt_neg(file: str, path: str, password: str, exp):
    with exp:
        async with async_session_maker() as session:
            await encrypt(dir_=path, file_name=file, base_path=config_test.BASE_TEST_PATH,
                          password=password, session=session)
