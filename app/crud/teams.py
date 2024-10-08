from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from models.models import Team, TeamCreate

# Get all teams
async def get_teams(db: AsyncSession) -> List[Team]:
    try:
        result = await db.execute(select(Team))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a team by ID
async def get_team_by_id(db: AsyncSession, team_id: int) -> Team:
    try:
        result = await db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        if team is None:
            raise HTTPException(status_code=404, detail="Not found team.")
        return team
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a team
async def create_team(db: AsyncSession, new_team: TeamCreate) -> Dict[str, int]:
    try:
        team = Team(name=new_team.name)
        db.add(team)
        await db.commit()
        await db.refresh(team)
        return team
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update a team
async def update_team(db: AsyncSession, updated_team: TeamCreate, team_id: int) -> None:
    try:
        team = await get_team_by_id(db, team_id)
        if team is None:
            raise HTTPException(status_code=404, detail="Not found team.")

        team.name = updated_team.name

        await db.commit()
        await db.refresh(team)
        return team
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a team
async def delete_team(db: AsyncSession, team_id: int) -> None:
    try:
        team = await get_team_by_id(db, team_id)
        if team is None:
            raise HTTPException(status_code=404, detail="Not found team.")

        await db.delete(team)
        await db.commit()
        return {"detail": "Team with id " + str(team_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Other gets
# Get teams by name
async def get_team_by_name(db: AsyncSession, name: str) -> List[Team]:  # Changed return type to List[Team]
    try:
        result = await db.execute(select(Team).where(Team.name.ilike(f"%{name}%")))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))