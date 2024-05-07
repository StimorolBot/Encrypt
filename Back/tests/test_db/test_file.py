from tests.conftest import async_session_maker
from src.app.encrypt.file_manager import file_manager


async def test_add_file():
    async with async_session_maker() as session:
        result = file_manager.add_file(session=session, file_name="", email="")
        assert result is None


"""
    async def add_file(self, session: "AsyncSession", file_name: str, email: "EmailStr", file: "UploadFile",
                       field, table: "DeclarativeAttributeIntercept" = FileTable, value: str = ""):
        file_list = await self.get_exists_files(session=session, table=table, field=field, value=file_name)
"""