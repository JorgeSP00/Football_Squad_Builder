from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.nationalities import create_nationality, delete_nationality, get_nationalities, get_nationalities_by_name, get_nationality_by_id, update_nationality
from db import get_db
from models.models import NationalityCreate

router=APIRouter()

# Nationalities Endpoints
@router.get("/nationalities/")
async def read_nationalities(db: AsyncSession = Depends(get_db)):
    return {"nationalities": await get_nationalities(db)}

@router.get("/nationalities/{nationality_id}")
async def read_nationality(nationality_id: int, db: AsyncSession = Depends(get_db)):
    return await get_nationality_by_id(db, nationality_id)

@router.post("/nationalities/")
async def create_nationality_route(nationality: NationalityCreate, db: AsyncSession = Depends(get_db)):
    return await create_nationality(db, nationality)

@router.put("/nationalities/{nationality_id}")
async def update_nationality_route(nationality: NationalityCreate, nationality_id: int, db: AsyncSession = Depends(get_db)):
    return await update_nationality(db, nationality, nationality_id)
    

@router.delete("/nationalities/{nationality_id}")
async def delete_nationality_route(nationality_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_nationality(db, nationality_id)

@router.get("/nationalities_filtered/")
async def read_nationalities_name(name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if name:
        return await get_nationalities_by_name(db, name)
    else:
        raise HTTPException(status_code=400, detail="Please provide a filter parameter: name")

