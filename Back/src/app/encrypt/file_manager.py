import os
import aiofiles
from typing import TYPE_CHECKING
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.config import config
from core.operations.crud import Crud
from src.app.auth.models.user import UserTable
from src.app.encrypt.models.model import PathTable, FileTable

if TYPE_CHECKING:
    from pydantic import EmailStr
    from fastapi import UploadFile
    from sqlalchemy.ext.asyncio import AsyncSession


class FileManager:
    @classmethod
    async def check_dir(cls, file_path: str, session: "AsyncSession", data: dict):
        if os.path.exists(file_path) is False:
            os.mkdir(file_path)
            await Crud.create(session=session, table=PathTable, data_dict=data)

    async def save_file(self, dir_: "EmailStr", file_name: str, file: "UploadFile", session: "AsyncSession"):
        path = f"{config.BASE_PATH}/{dir_}"
        await self.check_dir(path, session, data={"email": dir_, "path": path})
        async with aiofiles.open(f"{path}/{file_name}", "wb") as f:
            content = await file.read()
            await f.write(content)
        print(f"Файл '{file_name}' сохранен в: {path}/")

    @staticmethod
    async def get_info(session: "AsyncSession", email: "EmailStr"):
        query = (select(UserTable, PathTable)
                 .options(selectinload(UserTable.path))
                 .options(selectinload(PathTable.file_name))
                 ).where(UserTable.email == email)
        res = await session.execute(query)
        return res.unique().scalars().all()

    @classmethod
    async def get_file_info(cls, session: "AsyncSession", file_name: str):
        query = (select(PathTable, FileTable).options(selectinload(PathTable.file_name))).where(FileTable.name == file_name)
        res = await session.execute(query)
        return res.unique().scalars().all()

    async def check_exists_file(self, session: "AsyncSession", file_name: str):
        current_file = await self.get_file_info(session=session, file_name=file_name)
        if len(current_file) != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл с таким именем уже существует")
