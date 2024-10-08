from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from models.models import SquadPlayer, SquadPlayerCreate

# Get all squad players
async def get_squad_players(db: AsyncSession) -> List[SquadPlayer]:
    try:
        result = await db.execute(select(SquadPlayer))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a squad player by ID
async def get_squad_player_by_id(db: AsyncSession, squad_player_id: int) -> SquadPlayer:
    try:
        result = await db.execute(select(SquadPlayer).where(SquadPlayer.id == squad_player_id))
        squad_player = result.scalar_one_or_none()
        if squad_player is None:
            raise HTTPException(status_code=404, detail="Not found player-squad")
        return squad_player
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a squad player
async def create_squad_player(db: AsyncSession, new_squad: SquadPlayerCreate) -> Dict[str, int]:
    try:
        squad_player = SquadPlayer(squad_id=new_squad.squad_id, player_id=new_squad.player_id, position=new_squad.position)
        db.add(squad_player)
        await db.commit()
        await db.refresh(squad_player)
        return squad_player
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update a squad player
async def update_squad_player(db: AsyncSession, updated_squad_player: SquadPlayerCreate, squad_player_id: int) -> None:
    try:
        squad_player = await get_squad_player_by_id(db, squad_player_id)
        if squad_player is None:
            raise HTTPException(status_code=404, detail="Not found player-squad")

        squad_player.squad_id = updated_squad_player.squad_id
        squad_player.player_id = updated_squad_player.player_id
        squad_player.position = updated_squad_player.position

        await db.commit()
        
        await db.refresh(squad_player)
        return squad_player
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update player-squad: " + str(e))

# Delete a squad player
async def delete_squad_player(db: AsyncSession, squad_player_id: int) -> None:
    try:
        squad_player = await get_squad_player_by_id(db, squad_player_id)
        if squad_player is None:
            raise HTTPException(status_code=404, detail="Not found player-squad")

        await db.delete(squad_player)
        await db.commit()
        return {"detail": "Squad-player with id " + str(squad_player_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get squad players by squad ID
async def get_squad_player_by_squad_id(db: AsyncSession, squad_id: int) -> SquadPlayer:
    try:
        result = await db.execute(select(SquadPlayer).where(SquadPlayer.squad_id == squad_id))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))