from fastapi import Request
from fastapi import APIRouter
from core.config import template

router = APIRouter(tags=["encrypt"])


@router.get("/")
async def get_home_page(request: Request):
    return template.TemplateResponse("/main.html", {"request": request})
