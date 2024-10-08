from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from models.models import Nationality, NationalityCreate

# Get all nationalities
async def get_nationalities(db: AsyncSession) -> List[Nationality]:
    try:
        result = await db.execute(select(Nationality))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a nationality by ID
async def get_nationality_by_id(db: AsyncSession, nationality_id: int) -> Nationality:
    try:
        result = await db.execute(select(Nationality).where(Nationality.id == nationality_id))
        nationality = result.scalar_one_or_none()
        if nationality is None:
            raise HTTPException(status_code=404, detail="Not found nationality")
        return nationality
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new nationality
async def create_nationality(db: AsyncSession, new_nationality: NationalityCreate) -> Dict[str, int]:
    try:
        nationality = Nationality(name=new_nationality.name)
        db.add(nationality)
        await db.commit()
        await db.refresh(nationality)
        return nationality
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update an existing nationality
async def update_nationality(db: AsyncSession, updated_nationality: NationalityCreate, nationality_id: int) -> None:
    try:
        nationality = await get_nationality_by_id(db, nationality_id)
        if nationality is None:
            raise HTTPException(status_code=404, detail="Not found nationality")

        nationality.name = updated_nationality.name

        await db.commit()
        
        await db.refresh(nationality)
        return nationality
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update nationality: " + str(e))

# Delete a nationality
async def delete_nationality(db: AsyncSession, nationality_id: int) -> None:
    try:
        nationality = await get_nationality_by_id(db, nationality_id)
        if nationality is None:
            raise HTTPException(status_code=404, detail="Not found nationality")

        await db.delete(nationality)
        await db.commit()
        return {"detail": "Nationality with id " + str(nationality_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Other get functions
# Get nationalities by name
async def get_nationalities_by_name(db: AsyncSession, name: str) -> Nationality:
    try:
        result = await db.execute(select(Nationality).where(Nationality.name.ilike(f"%{name}%")))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))