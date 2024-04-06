from typing import TYPE_CHECKING
from fastapi.responses import FileResponse
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException, status, Depends

from core.operations.crud import Crud
from core.db import get_async_session
from core.config import template, config
from core.operations.operation import save_file

from src.app.encrypt.operations import encrypt
from src.app.auth.user_manager import UserManager
from src.app.encrypt.models.model import FileTable
from src.app.encrypt.schemas.schemas import EncryptSchemas

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["encrypt"])


@router.get("/") #current_user: dict = Depends(UserManager.get_current_user),
async def get_home_page(request: Request,
                        session: "AsyncSession" = Depends(get_async_session)):
    await Crud.read_all(table=FileTable, session=session)
    return template.TemplateResponse("/index.html", {"request": request})


@router.post("/file", status_code=status.HTTP_200_OK)
async def file_operations(password: str = Form(...), upload_file: UploadFile = File(...),
                          current_user: dict = Depends(UserManager.get_current_user),
                          session: "AsyncSession" = Depends(get_async_session)):
    file_name = upload_file.filename
    EncryptSchemas(file_name=file_name, file_size=upload_file.size, password=password)
    file_path = f"{config.BASE_PATH}/{current_user['email']}"
    current_file = await Crud.read_one(session=session, table=FileTable, field=FileTable.file_name, value=file_name)

    if current_file is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл с таким именем уже существует")
    await save_file(file_name=file_name, file_path=file_path, file=upload_file.file.read())

    try:
        path = encrypt(file_path=f"{file_path}/{file_name}", password=password)
        data = {"user_id": current_user["id"], "path": file_path, "file_name": file_name}
        await Crud.create(session=session, table=FileTable, data_dict=data)
        return FileResponse(path=path, filename=path, media_type='multipart/form-data')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")
