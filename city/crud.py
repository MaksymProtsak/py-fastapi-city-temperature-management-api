from sqlalchemy.future import select

from . import models


async def get_all_cities(db):
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()
