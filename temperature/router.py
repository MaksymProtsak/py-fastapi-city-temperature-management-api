from fastapi import HTTPException
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from dependencies import get_db

from temperature import schemas, crud
from city.crud import get_city

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature]
)
async def read_temperatures(db: Session = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_temperature(
        temperature: schemas.TemperatureCreate,
        db: Session = Depends(get_db)
):
    db_temperature = await crud.get_temperature_by_city_id(
        db=db, city_id=temperature.city_id
    )
    city = await get_city(db=db, city_id=temperature.city_id)
    if city is None:
        raise HTTPException(
            status_code=400, detail="City not exist"
        )
    if db_temperature:
        raise HTTPException(
            status_code=400, detail="Temperature for city already exists"
        )

    result = await crud.create_temperature(
        db=db,
        temperature=temperature
    )
    return result
