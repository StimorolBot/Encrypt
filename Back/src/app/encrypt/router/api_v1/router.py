from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, Request, UploadFile, File

from core.config import template
from core.operation import save_file
from src.app.encrypt.operations import encrypt
from src.app.encrypt.schemas.schemas import PasswordSchemas, FileSchemas

router = APIRouter(tags=["encrypt"])


@router.get("/")
async def get_home_page(request: Request):
    return template.TemplateResponse("/main.html", {"request": request})


@router.post("/file", status_code=status.HTTP_200_OK)
async def file_operations(password: PasswordSchemas = Depends(), file: UploadFile = File(...)):
    FileSchemas(name=file.filename, size=file.size)
    await save_file(file_name=file.filename, file_path="save_file", file=file.file.read())
    try:
        path = encrypt(file_path=f"save_file/{file.filename}", password=password.password)
        return FileResponse(path=path, filename=path, media_type='multipart/form-data')

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")
