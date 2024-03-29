from fastapi import APIRouter

router = APIRouter(tags=["encrypt"])


@router.get("/")
async def get_home_page():
    return "home page"
