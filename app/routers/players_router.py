from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.players import create_player, delete_player, get_player_by_id, get_players, get_players_with_filters, update_player
from db import get_db
from models.models import PlayerCreate

router=APIRouter()

#Players Endpoints
@router.get("/players/")
async def read_players(db: AsyncSession = Depends(get_db)):
    return {"players": await get_players(db)}

@router.get("/players/{player_id}")
async def read_player(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_player_by_id(db, player_id)

@router.post("/players/")
async def create_player_route(player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    return await create_player(db, player)

@router.put("/players/{player_id}")
async def update_player_route(player: PlayerCreate, player_id: int, db: AsyncSession = Depends(get_db)):
    return await update_player(db, player, player_id)
    
@router.delete("/players/{player_id}")
async def delete_player_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_player(db, player_id)

@router.get("/players_filtered/")
async def read_players_filtered(nationality_id: Optional[int] = None, competition_id: Optional[int] = None, team_id: Optional[int] = None, market_value: Optional[float] = None,
                                position: Optional[str] = None,name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if nationality_id or name or competition_id or team_id or market_value or position:
        return await get_players_with_filters(db, nationality_id, name, team_id, competition_id, market_value, position)
    else:
        return await get_players(db)

