from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.competitions import create_competition, delete_competition, get_competition_by_id, get_competition_by_name, get_competitions, update_competition
from db import get_db
from models.models import CompetitionCreate

router=APIRouter()

# Competitions Endpoints
@router.get("/competitions/")
async def read_competitions(db: AsyncSession = Depends(get_db)):
    return {"competitions": await get_competitions(db)}

@router.get("/competitions/{competition_id}")
async def read_competition(competition_id: int, db: AsyncSession = Depends(get_db)):
    return await get_competition_by_id(db, competition_id)

@router.post("/competitions/")
async def create_competition_route(competition: CompetitionCreate, db: AsyncSession = Depends(get_db)):
    return await create_competition(db, competition)

@router.put("/competitions/{competition_id}")
async def update_competition_route(competition_id: int, competition: CompetitionCreate, db: AsyncSession = Depends(get_db)):
    return await update_competition(db, competition, competition_id)
    

@router.delete("/competitions/{competition_id}")
async def delete_competition_route(competition_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_competition(db, competition_id)


@router.get("/competitions_filtered/")
async def read_competition_name(name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if name:
        return await get_competition_by_name(db, name)
    else:
        raise HTTPException(status_code=400, detail="Please provide a filter parameter: name")