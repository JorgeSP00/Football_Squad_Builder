from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from models.models import TeamCompetition, TeamCompetitionCreate

# Get all team competitions
async def get_team_competitions(db: AsyncSession) -> List[TeamCompetition]:
    try:
        result = await db.execute(select(TeamCompetition))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get competitions a team is participating in by team ID
async def get_team_in_competitions_by_team_id(db: AsyncSession, team_id: int) -> TeamCompetition:
    try:
        team_competitions = await db.execute(select(TeamCompetition).where(TeamCompetition.team_id == team_id))
        if team_competitions is None:
            raise HTTPException(status_code=404, detail="Could not find which competition this team plays.")
        return team_competitions.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Get participants in a competition by competition ID
async def get_competition_participants_by_competition_id(db: AsyncSession, competition_id: int) -> TeamCompetition:
    try:
        competition_participants = await db.execute(select(TeamCompetition).where(TeamCompetition.competition_id == competition_id))
        if competition_participants is None:
            raise HTTPException(status_code=404, detail="Could not find participants for this competition.")
        return competition_participants.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get team competition by team ID and competition ID
async def get_team_competition_by_team_id_competition_id(db: AsyncSession, team_id: int, competition_id: int) -> TeamCompetition:
    try:
        result = await db.execute(select(TeamCompetition).where((TeamCompetition.competition_id == competition_id) & (TeamCompetition.team_id == team_id)))
        team_competition = result.scalar_one_or_none()
        if team_competition is None:
            raise HTTPException(status_code=404, detail="Could not find information for team-competition.")
        return team_competition
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a team competition
async def create_team_competition(db: AsyncSession, new_team_competition: TeamCompetitionCreate) -> Dict[str, int]:
    try:
        team_competition = TeamCompetition(
            team_id=new_team_competition.team_id,
            competition_id=new_team_competition.competition_id
        )
        db.add(team_competition)
        await db.commit()
        
        await db.refresh(team_competition)
        return team_competition
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a team competition
async def delete_team_competition(db: AsyncSession, team_id: int, competition_id: int) -> None:
    try:
        team_competition = await get_team_competition_by_team_id_competition_id(db, team_id, competition_id)
        if team_competition is None:
            raise HTTPException(status_code=404, detail="Could not find information for team-competition.")

        await db.delete(team_competition)
        await db.commit()
        return {"detail": "Team-Competition with team id " + str(team_id) + " and competition id " + str(competition_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))