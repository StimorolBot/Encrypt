import aiofiles


async def save_file(file_name: str, file):
    async with aiofiles.open(f"save_file/{file_name}", "wb") as f:
        await f.write(file)
