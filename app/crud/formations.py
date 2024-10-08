from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from models.models import Formation, FormationCreate

# Get all formations
async def get_formations(db: AsyncSession) -> List[Formation]:
    try:
        result = await db.execute(select(Formation))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a formation by ID
async def get_formation_by_id(db: AsyncSession, formation_id: int) -> Formation:
    try:
        result = await db.execute(select(Formation).where(Formation.id == formation_id))
        formation = result.scalar_one_or_none()
        if formation is None:
            raise HTTPException(status_code=404, detail="Not found formation")
        return formation
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new formation
async def create_formation(db: AsyncSession, new_formation: FormationCreate) -> Dict[str, int]:
    try:
        formation = Formation(name=new_formation.name, description=new_formation.description)
        db.add(formation)
        await db.commit()
        await db.refresh(formation)
        return formation
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update an existing formation
async def update_formation(db: AsyncSession, updated_formation: FormationCreate, formation_id: int) -> None:
    try:
        formation = await get_formation_by_id(db, formation_id)
        if formation is None:
            raise HTTPException(status_code=404, detail="Not found formation")

        formation.name = updated_formation.name
        formation.description = updated_formation.description
        await db.commit()
        
        await db.refresh(formation)
        return formation
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update formation: " + str(e))

# Delete a formation
async def delete_formation(db: AsyncSession, formation_id: int) -> None:
    try:
        formation = await get_formation_by_id(db, formation_id)
        if formation is None:
            raise HTTPException(status_code=404, detail="Not found formation")

        await db.delete(formation)
        await db.commit()
        return {"detail": "Formation with id " + str(formation_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))