from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.squads import create_squad, delete_squad, get_squad_by_id, get_squad_with_filters, get_squads, update_squad
from db import get_db
from models.models import SquadCreate

router=APIRouter()

# Squads Endpoints
@router.get("/squads/")
async def read_squads(db: AsyncSession = Depends(get_db)):
    return {"squads": await get_squads(db)}

@router.get("/squads/{squad_id}")
async def read_squad(squad_id: int, db: AsyncSession = Depends(get_db)):
    return await get_squad_by_id(db, squad_id)

@router.post("/squads/")
async def create_squad_route(squad: SquadCreate, db: AsyncSession = Depends(get_db)):
    return await create_squad(db, squad)

@router.put("/squads/{squad_id}")
async def update_squad_route(squad: SquadCreate, squad_id: int, db: AsyncSession = Depends(get_db)):
    return await update_squad(db, squad, squad_id)
    

@router.delete("/squads/{squad_id}")
async def delete_squad_route(squad_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_squad(db, squad_id)

@router.get("/squads_filtered/")
async def read_squads_filtered(user_id: Optional[int] = None, name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if user_id or name:
        return await get_squad_with_filters(db, user_id, name)
    else:
        raise HTTPException(status_code=400, detail="Please provide a filter parameter: name or user")