import aiofiles
from uuid import uuid4


async def save_file(file_name: str, file_path: str, file):
    async with aiofiles.open(f"{file_path}/{file_name}", "wb") as f:
        await f.write(file)


def generate_uuid():
    return str(uuid4())