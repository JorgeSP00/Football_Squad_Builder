from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud.team_competitions import create_team_competition, delete_team_competition, get_competition_participants_by_competition_id, get_team_competition_by_team_id_competition_id, get_team_competitions, get_team_in_competitions_by_team_id
from db import get_db
from models.models import TeamCompetitionCreate

router=APIRouter()

# TeamCompetitions Endpoints
@router.get("/teams_competitions/")
async def read_team_competitions(db: AsyncSession = Depends(get_db)):
    return {"team_competitions": await get_team_competitions(db)}

@router.get("/teams_competitions/{team_id}/{competition_id}")
async def read_team_competition(team_id: int, competition_id: int, db: AsyncSession = Depends(get_db)):
    return await get_team_competition_by_team_id_competition_id(db, team_id, competition_id)

@router.get("/team_competitions/{team_id}")
async def read_team_in_competitions(team_id: int, db: AsyncSession = Depends(get_db)):
    return await get_team_in_competitions_by_team_id(db, team_id)

@router.get("/competition_participants/{competition_id}")
async def read_competition_participants(competition_id: int, db: AsyncSession = Depends(get_db)):
    return await get_competition_participants_by_competition_id(db, competition_id)

@router.post("/teams_competitions/")
async def create_team_competition_route(team_competition: TeamCompetitionCreate, db: AsyncSession = Depends(get_db)):
    return await create_team_competition(db, team_competition)

@router.delete("/teams_competitions/{team_id}/{competition_id}")
async def delete_team_competition_route(team_id: int, competition_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_team_competition(db, team_id, competition_id)