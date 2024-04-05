import os
import aiofiles
from uuid import uuid4


async def check_dir(file_path: str):
    if os.path.isdir(file_path) is False:
        os.mkdir(file_path)


async def save_file(file_name: str, file_path: str, file):
    await check_dir(file_path)
    async with aiofiles.open(f"{file_path}/{file_name}", "wb") as f:
        await f.write(file)


def generate_uuid():
    return str(uuid4())
