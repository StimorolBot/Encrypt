from typing import TYPE_CHECKING
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, Form, status, Depends, Request

from core.db import get_async_session

from src.app.encrypt.operations import encrypt
from src.app.auth.user_manager import UserManager
from src.app.encrypt.file_manager import FileManager
from src.app.encrypt.schemas.schemas import EncryptSchemas

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.app.auth.schemas.auth import UserRead

router = APIRouter(tags=["encrypt"])


@router.get("/")
async def get_home_page(re: Request, token: dict = Depends(UserManager.get_jwt_token), session: "AsyncSession" = Depends(get_async_session), ):
    print(re.cookies["access_token"]) #
    return await FileManager.get_info(session=session, email=token["email"])


@router.post("/file", status_code=status.HTTP_200_OK)
async def file_operations(password: str = Form(...), upload_file: UploadFile = File(...),
                          current_user: "UserRead" = Depends(UserManager.get_current_user),
                          session: "AsyncSession" = Depends(get_async_session)) -> FileResponse:
    EncryptSchemas(file_name=upload_file.filename, file_size=upload_file.size, password=password)
    await FileManager().check_exists_file(session=session, file_name=upload_file.filename, dir_=current_user.email)
    await FileManager().save_file(dir_=current_user.email, file_name=upload_file.filename, file=upload_file, session=session)
    output_path, output_file = await encrypt(dir_=current_user.email, file_name=upload_file.filename, password=password)
    return FileResponse(path=output_path, filename=output_file, media_type='multipart/form-data')
