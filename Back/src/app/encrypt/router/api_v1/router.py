from fastapi import Request, UploadFile
from core.config import template
from fastapi import APIRouter, Depends
from src.app.encrypt.schemas.schemas import CheckPassword

router = APIRouter(tags=["encrypt"])


@router.get("/")
async def get_home_page(request: Request):
    return template.TemplateResponse("/main.html", {"request": request})


@router.post("/encrypt-file")
async def encrypt_file(file: UploadFile, password=Depends(CheckPassword)):
    return file
