from typing import TYPE_CHECKING, Literal
from sqlalchemy import select, func, update, delete

from fastapi import HTTPException, status

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


class Crud:
    @staticmethod
    async def create(session: "AsyncSession", data_dict: dict,
                     table: "DeclarativeAttributeIntercept") -> "DeclarativeAttributeIntercept":
        stmt = table(**data_dict)
        session.add(stmt)
        await session.commit()
        return stmt

    @staticmethod
    async def read(session: "AsyncSession", table: "DeclarativeAttributeIntercept",
                   field: "DeclarativeAttributeIntercept", value: str, mode: Literal["one", "all"] = "one"):
        query = select(table).where(func.lower(field) == func.lower(value))
        results = await session.execute(query)

        if mode == "one":
            return results.unique().scalar_one_or_none()

        elif mode == "all":
            return [item for items in results.all() for item in items]

    @staticmethod
    async def read_all(session: "AsyncSession", table: "DeclarativeAttributeIntercept"):
        query = select(table)
        results = await session.execute(query)
        return [item for items in results.all() for item in items]

    @staticmethod
    async def update(session: "AsyncSession", table: "DeclarativeAttributeIntercept", field, field_val, data: dict):
        query = update(table).where(func.lower(field) == func.lower(field_val)).values(**data)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def delete(session: "AsyncSession", table: "DeclarativeAttributeIntercept", field, field_val):
        stmt = delete(table).where(func.lower(field) == func.lower(field_val))
        await session.execute(stmt)
        await session.commit()
        return stmt

    @staticmethod
    async def read_and_create(session: "AsyncSession", table: "DeclarativeAttributeIntercept", field, value, detail_error: str, data_dict: dict):
        item = await Crud.read(session=session, table=table, value=value, field=field)
        if item:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail_error)
        await Crud.create(session=session, table=table, data_dict=data_dict)
