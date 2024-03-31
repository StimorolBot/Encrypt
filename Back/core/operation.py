import aiofiles


async def save_file(file_name: str, file_path: str, file):
    async with aiofiles.open(f"{file_path}/{file_name}", "wb") as f:
        await f.write(file)
