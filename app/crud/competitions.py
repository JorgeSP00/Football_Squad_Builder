from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from models.models import Competition, CompetitionCreate

# Get all competitions
async def get_competitions(db: AsyncSession) -> List[Competition]:
    try:
        result = await db.execute(select(Competition))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a competition by ID
async def get_competition_by_id(db: AsyncSession, comp_id: int) -> Competition:
    try:
        result = await db.execute(select(Competition).where(Competition.id == comp_id))
        competition = result.scalar_one_or_none()
        if competition is None:
            raise HTTPException(status_code=404, detail="Not found competition")
        return competition
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new competition
async def create_competition(db: AsyncSession, new_competition: CompetitionCreate) -> Dict[str, int]:
    try:
        competition = Competition(name=new_competition.name, region=new_competition.region)
        db.add(competition)
        await db.commit()
        await db.refresh(competition)
        return competition
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update an existing competition
async def update_competition(db: AsyncSession, competition: CompetitionCreate, competition_id: int) -> Competition:
    try:
        # Find the competition by ID
        competition_update = await get_competition_by_id(db, competition_id)

        # Check if the competition exists
        if competition_update is None:
            raise HTTPException(status_code=404, detail="Not found competition")

        # Update only the provided fields
        competition_update.name = competition.name
        competition_update.region = competition.region

        # Save changes
        await db.commit()
        
        await db.refresh(competition_update)
        # Return the updated competition
        return competition_update
    except SQLAlchemyError as e:
        # Rollback in case of error
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update competition: " + str(e))

# Delete a competition
async def delete_competition(db: AsyncSession, comp_id: int) -> None:
    try:
        competition = await get_competition_by_id(db, comp_id)
        if competition is None:
            raise HTTPException(status_code=404, detail="Not found competition")

        await db.delete(competition)
        await db.commit()
        return {"detail": "Competition with id " + str(comp_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

# Other get functions
# Get competitions by name
async def get_competition_by_name(db: AsyncSession, name: str) -> Competition:
    try:
        result = await db.execute(select(Competition).where(Competition.name.ilike(f"%{name}%")))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))