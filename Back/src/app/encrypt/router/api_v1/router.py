from typing import TYPE_CHECKING
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, Form, status, Depends, HTTPException

from core.db import get_async_session
from core.operations.crud import Crud
from core.setting import http_bearer, setting

from src.app.auth.user_manager import UserManager

from src.app.encrypt.operations import encrypt
from src.app.encrypt.models.model import FileTable
from src.app.encrypt.schemas.encrypt import EncryptSchemas
from src.app.encrypt.schemas.file import FileDTO, FileName
from src.app.encrypt.file_manager import file_manager, FileManager

if TYPE_CHECKING:
    from src.app.auth.schemas.auth import UserRead
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Home"], dependencies=[Depends(http_bearer)])
encrypt_router = APIRouter(tags=["encrypt"], prefix="/file", dependencies=[Depends(http_bearer)])


@router.get("/")
async def get_home_page(current_user: "UserRead" = Depends(UserManager.get_current_user),
                        session: "AsyncSession" = Depends(get_async_session)) -> list:
    file_info = await FileManager.get_all_info(session=session, email=current_user.email)
    return [FileDTO.model_validate(item, from_attributes=True) for item in file_info]


@encrypt_router.post("", status_code=status.HTTP_200_OK)
async def upload_file(password: str = Form(...), file: UploadFile = File(...),
                      current_user: "UserRead" = Depends(UserManager.get_current_user),
                      session: "AsyncSession" = Depends(get_async_session)) -> FileResponse:
    EncryptSchemas(file_name=file.filename, file_size=file.size, password=password)
    await file_manager.save_file(dir_=current_user.email, file_name=file.filename, file=file, session=session)
    output_path, output_file = await encrypt(dir_=current_user.email, file_name=file.filename, password=password, session=session)

    return FileResponse(path=output_path, filename=output_file, media_type='multipart/form-data',
                        headers={"Content-Disposition": output_file})


@encrypt_router.delete("/file-delete", status_code=status.HTTP_200_OK)
async def delete_file(name: FileName, session: "AsyncSession" = Depends(get_async_session)):
    await Crud.delete(session=session, table=FileTable, field=FileTable.name, field_val=name.name)
    return f"Файл {name.name} удален"


@encrypt_router.get("/download/{path}/{file_name}")
async def download_file(path: str, file_name: str, current_user: "UserRead" = Depends(UserManager.get_current_user)) -> FileResponse:
    if current_user.email == path:
        return FileResponse(path=f"{setting.base_path}/{path}/{file_name}", filename=file_name, media_type='multipart/form-data')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не удалось найти страницу")
