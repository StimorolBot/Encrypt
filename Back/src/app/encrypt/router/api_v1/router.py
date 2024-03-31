from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, Request, UploadFile, File

from core.config import template
from core.operation import save_file
from src.app.encrypt.operation.encode_file import encrypt
from src.app.encrypt.schemas.schemas import PasswordSchemas

router = APIRouter(tags=["encrypt"])


@router.get("/")
async def get_home_page(request: Request):
    return template.TemplateResponse("/main.html", {"request": request})


@router.post("/encrypt-file")
async def encrypt_file(file: UploadFile = File(...), password: PasswordSchemas = Depends()):
    await save_file(file_name=file.filename, file_path="save_file", file=file.file.read())
    path = encrypt(file_path=f"save_file/{file.filename}", password=password.password)
    return FileResponse(path=path, filename=f"{file.filename}.aes", media_type='multipart/form-data')
