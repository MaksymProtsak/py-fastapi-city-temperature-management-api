from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db

from city import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Session = Depends(get_db)):
    return await crud.get_all_cities(db=db)
