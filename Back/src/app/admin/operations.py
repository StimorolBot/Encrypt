from fastapi import status, HTTPException
from datetime import timezone, datetime, timedelta
from src.app.admin.schemas.schemas import DateType


async def get_date(date: int, type_date: str) -> datetime:
    now = datetime.now(timezone.utc)

    match type_date:
        case DateType.seconds.value:
            block_date = now + timedelta(seconds=date)
        case DateType.hours.value:
            block_date = now + timedelta(hours=date)
        case DateType.days.value:
            block_date = now + timedelta(days=date)
        case DateType.months.value:
            month = date * 30.4
            block_date = now + timedelta(days=month)
        case DateType.years.value:
            year = date * 365
            block_date = now + timedelta(days=year)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Ожидалось: 'seconds', 'hours', 'days', 'months' или 'years"
                                )

    return block_date.replace(tzinfo=None)
