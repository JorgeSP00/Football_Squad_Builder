from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.teams import create_team, delete_team, get_team_by_id, get_team_by_name, get_teams, update_team
from db import get_db
from models.models import TeamCreate

router=APIRouter()

# Teams Endpoints
@router.get("/teams/")
async def read_teams(db: AsyncSession = Depends(get_db)):
    return {"teams": await get_teams(db)}

@router.get("/teams/{team_id}")
async def read_team(team_id: int, db: AsyncSession = Depends(get_db)):
    return await get_team_by_id(db, team_id)

@router.post("/teams/")
async def create_team_route(team: TeamCreate, db: AsyncSession = Depends(get_db)):
    return await create_team(db, team)

@router.put("/teams/{team_id}")
async def update_team_route(team: TeamCreate, team_id: int, db: AsyncSession = Depends(get_db)):
    return await update_team(db, team, team_id)
    

@router.delete("/teams/{team_id}")
async def delete_team_route(team_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_team(db, team_id)

@router.get("/teams_filtered/")
async def read_team_name(name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if name:
        return await get_team_by_name(db, name)
    else:
        raise HTTPException(status_code=400, detail="Please provide a filter parameter: name")