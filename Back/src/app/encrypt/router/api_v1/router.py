from typing import TYPE_CHECKING
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, Form, status, Depends

from core.db import get_async_session

from core.setting import http_bearer
from src.app.encrypt.operations import encrypt
from src.app.auth.user_manager import UserManager
from src.app.encrypt.models.model import FileTable
from src.app.encrypt.file_manager import file_manager
from src.app.encrypt.schemas.schemas import EncryptSchemas

if TYPE_CHECKING:
    from src.app.auth.schemas.auth import UserRead
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["encrypt"], dependencies=[Depends(http_bearer)])


@router.get("/")
async def get_home_page(current_user: "UserRead" = Depends(UserManager.get_current_user),
                        session: "AsyncSession" = Depends(get_async_session)):
    file_info = await file_manager.get_exists_files(session=session, field=FileTable.email, value=current_user.email)
    return file_info


@router.post("/file", status_code=status.HTTP_200_OK)
async def upload_file(password: str = Form(...), file: UploadFile = File(...),
                      current_user: "UserRead" = Depends(UserManager.get_current_user),
                      session: "AsyncSession" = Depends(get_async_session)) -> FileResponse:  # -> dict:  #
    EncryptSchemas(file_name=file.filename, file_size=file.size, password=password)  # проверка пароля на запрещенные символы
    await file_manager.add_file(session=session, file_name=file.filename,
                                email=current_user.email, file=file, field=FileTable.name)
    output_path, output_file = await encrypt(dir_=current_user.email, file_name=file.filename, password=password, session=session)

    return FileResponse(path=output_path, filename=output_file, media_type='multipart/form-data',
                        headers={"Content-Disposition": output_file})


@router.get("/file/{download}/{file_name}")
async def download_file(download: str, file_name: str):
    # проверка пользователя и папки
    ...
