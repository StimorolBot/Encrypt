from typing import TYPE_CHECKING
from sqlalchemy import select, func
from core.config import pwd_context

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


class Crud:
    @staticmethod
    async def create(session: "AsyncSession", data_dict: dict,
                     table: "DeclarativeAttributeIntercept") -> "DeclarativeAttributeIntercept":
        if data_dict["password"]:
            data_dict["password"] = pwd_context.hash(data_dict["password"])

        stmt = table(**data_dict)
        session.add(stmt)
        await session.commit()
        return stmt

    @staticmethod
    async def read_one(session: "AsyncSession", table: "DeclarativeAttributeIntercept",
                       field: "DeclarativeAttributeIntercept", value: str):
        query = select(table).where(func.lower(field) == func.lower(value))
        results = await session.execute(query)
        return results.unique().scalar_one_or_none()
