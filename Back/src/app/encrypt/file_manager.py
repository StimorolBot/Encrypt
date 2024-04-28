import os
import aiofiles
from typing import TYPE_CHECKING
from fastapi import HTTPException, status

from core.setting import setting
from core.logger import os_logger
from core.operations.crud import Crud
from src.app.encrypt.models.model import PathTable, FileTable

if TYPE_CHECKING:
    from pydantic import EmailStr
    from fastapi import UploadFile
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


class FileManager:

    @classmethod
    async def check_dir(cls, file_path: str, session: "AsyncSession", data: dict):
        if os.path.exists(file_path) is False:
            os.mkdir(file_path)
            await Crud.create(session=session, table=PathTable, data_dict=data)

    async def save_file(self, dir_: "EmailStr", file_name: str, file: "UploadFile", session: "AsyncSession", base_path: str = setting.base_path):
        path = f"{base_path}/{dir_}"
        await self.check_dir(path, session, data={"email": dir_, "path": path})
        async with aiofiles.open(f"{path}/{file_name}", "wb") as f:
            content = await file.read()
            await f.write(content)
        os_logger.info(f"Файл '{file_name}' сохранен в: {path}/")

    async def add_file(self, session: "AsyncSession", file_name: str, email: "EmailStr", file: "UploadFile",
                       field, table: "DeclarativeAttributeIntercept" = FileTable):
        file_list = await Crud.read(session=session, table=table, value=file_name, field=field)

        if file_list:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл с таки именем уже существует")

        await self.save_file(dir_=email, file_name=file_name, session=session, file=file)


file_manager = FileManager()

"""
    @staticmethod
    async def get_info(session: "AsyncSession", email: "EmailStr"):
        query = (select(UserTable, PathTable)
                 .options(selectinload(UserTable.path))
                 .options(selectinload(PathTable.file_name))
                 ).where(UserTable.email == email)
        res = await session.execute(query)
        return res.unique().scalars().all()
"""
