from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db

from city import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Session = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = await crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city
