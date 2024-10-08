from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from models.models import Squad, SquadCreate

# Get all squads
async def get_squads(db: AsyncSession) -> List[Squad]:
    try:
        result = await db.execute(select(Squad))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a squad by ID
async def get_squad_by_id(db: AsyncSession, squad_id: int) -> Squad:
    try:
        result = await db.execute(select(Squad).where(Squad.id == squad_id))
        squad = result.scalar_one_or_none()
        if squad is None:
            raise HTTPException(status_code=404, detail="Not found squad")
        return squad
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a squad
async def create_squad(db: AsyncSession, new_squad: SquadCreate) -> Dict[str, int]:
    try:
        squad = Squad(
            user_id=new_squad.user_id,
            formation_id=new_squad.formation_id,
            name=new_squad.name,
            competition_id=new_squad.competition_id,
            budget=new_squad.budget,
            nationality_id=new_squad.nationality_id
        )
        db.add(squad)
        await db.commit()
        await db.refresh(squad)
        return squad
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update a squad
async def update_squad(db: AsyncSession, updated_squad: SquadCreate, squad_id: int) -> None:
    try:
        squad = await get_squad_by_id(db, squad_id)
        if squad is None:
            raise HTTPException(status_code=404, detail="Not found squad")

        squad.user_id = updated_squad.user_id
        squad.formation_id = updated_squad.formation_id
        squad.name = updated_squad.name
        squad.competition_id = updated_squad.competition_id
        squad.budget = updated_squad.budget
        squad.nationality_id = updated_squad.nationality_id

        await db.commit()
        await db.refresh(squad)
        return squad
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update squad: " + str(e))

# Delete a squad
async def delete_squad(db: AsyncSession, squad_id: int) -> None:
    try:
        squad = await get_squad_by_id(db, squad_id)
        if squad is None:
            raise HTTPException(status_code=404, detail="Not found squad")

        await db.delete(squad)
        await db.commit()
        return {"detail": "Squad with id " + str(squad_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get squad by name
async def get_squad_by_name(db: AsyncSession, name: str) -> Squad:
    try:
        result = await db.execute(select(Squad).where(Squad.name.ilike(f"%{name}%")))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get squads by user ID
async def get_squad_by_user(db: AsyncSession, user_id: int) -> Squad:
    try:
        result = await db.execute(select(Squad).where(Squad.user_id == user_id))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get squads with filters
async def get_squad_with_filters(db: AsyncSession, user_id: Optional[int] = None, name: Optional[str] = None, **filters):
    # Start the base query
    query = select(Squad)

    # List of dynamic conditions
    conditions = []

    # Add conditions only if values are not None
    if user_id is not None:
        conditions.append(Squad.user_id == user_id)
    if name is not None:
        conditions.append(Squad.name.ilike(f"%{name}%"))

    # Add more filters if passed through **filters
    for field, value in filters.items():
        if value is not None:
            # Use getattr to access the Squad model field
            conditions.append(getattr(Squad, field) == value)

    # Apply all conditions dynamically
    if conditions:
        query = query.where(and_(*conditions))

    # Execute the query
    result = await db.execute(query)
    squads = result.scalars().all()
    return squads