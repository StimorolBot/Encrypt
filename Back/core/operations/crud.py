from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


class Crud:
    @staticmethod
    async def create(session: "AsyncSession", data_dict: dict, table: "DeclarativeAttributeIntercept"):
        stmt = table(**data_dict)
        session.add(stmt)
        await session.commit()
