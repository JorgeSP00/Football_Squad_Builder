from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud.squad_players import create_squad_player, delete_squad_player, get_squad_player_by_id, get_squad_player_by_squad_id, get_squad_players, update_squad_player
from db import get_db
from models.models import SquadPlayerCreate

router=APIRouter()

# SquadPlayers Endpoints
@router.get("/squad_players/")
async def read_squad_players(db: AsyncSession = Depends(get_db)):
    return {"squad_players": await get_squad_players(db)}

@router.get("/squad_players/{squad_player_id}")
async def read_squad_player(squad_player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_squad_player_by_id(db, squad_player_id)

@router.post("/squad_players/")
async def create_squad_player_route(squad_player: SquadPlayerCreate, db: AsyncSession = Depends(get_db)):
    return await create_squad_player(db, squad_player)

@router.put("/squad_players/{squad_player_id}")
async def update_squad_player_route(squad_player: SquadPlayerCreate, squad_player_id: int, db: AsyncSession = Depends(get_db)):
    return await update_squad_player(db, squad_player, squad_player_id)
    

@router.delete("/squad_players/{squad_player_id}")
async def delete_squad_player_route(squad_player_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_squad_player(db, squad_player_id)

@router.get("/players_in_squad/{squad_id}")
async def read_squad_player(squad_id: int, db: AsyncSession = Depends(get_db)):
    return await get_squad_player_by_squad_id(db, squad_id)