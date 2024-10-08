from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud.formations import create_formation, delete_formation, get_formation_by_id, get_formations, update_formation
from db import get_db
from models.models import FormationCreate

router=APIRouter()

# Formations Endpoints
@router.get("/formations/")
async def read_formations(db: AsyncSession = Depends(get_db)):
    return {"formations": await get_formations(db)}

@router.get("/formations/{formation_id}")
async def read_formation(formation_id: int, db: AsyncSession = Depends(get_db)):
    return await get_formation_by_id(db, formation_id)

@router.post("/formations/")
async def create_formation_route(formation: FormationCreate, db: AsyncSession = Depends(get_db)):
    return await create_formation(db, formation)

@router.put("/formations/{formation_id}")
async def update_formation_route(formation: FormationCreate, formation_id: int, db: AsyncSession = Depends(get_db)):
    return await update_formation(db, formation, formation_id)
    

@router.delete("/formations/{formation_id}")
async def delete_formation_route(formation_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_formation(db, formation_id)