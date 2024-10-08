from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from models.models import Player, PlayerCreate, TeamCompetition

# Get all players
async def get_players(db: AsyncSession) -> List[Player]:
    try:
        result = await db.execute(select(Player))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a player by ID
async def get_player_by_id(db: AsyncSession, player_id: int) -> Player:
    try:
        result = await db.execute(select(Player).where(Player.id == player_id))
        player = result.scalar_one_or_none()
        if player is None:
            raise HTTPException(status_code=404, detail="Not found player")
        return player
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new player
async def create_player(db: AsyncSession, new_player: PlayerCreate) -> Dict[str, int]:
    try:
        player = Player(
            name=new_player.name, 
            team_id=new_player.team_id, 
            nationality_id=new_player.nationality_id, 
            market_value=new_player.market_value,
            position=new_player.position, 
            alternate_position=new_player.alternate_position
        )
        db.add(player)
        await db.commit()
        await db.refresh(player)
        return player
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update an existing player
async def update_player(db: AsyncSession, updated_player: PlayerCreate, player_id: int) -> None:
    try:
        player = await get_player_by_id(db, player_id)
        if player is None:
            raise HTTPException(status_code=404, detail="Not found player")

        player.name = updated_player.name
        player.team_id = updated_player.team_id
        player.nationality_id = updated_player.nationality_id
        player.market_value = updated_player.market_value
        player.position = updated_player.position
        player.alternate_position = updated_player.alternate_position

        await db.commit()
        
        await db.refresh(player)
        return player
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update player " + str(e))

# Delete a player
async def delete_player(db: AsyncSession, player_id: int) -> None:
    try:
        player = await get_player_by_id(db, player_id)
        if player is None:
            raise HTTPException(status_code=404, detail="Not found player")

        await db.delete(player)
        await db.commit()
        return {"detail": "Player with id " + str(player_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get players with filters
async def get_players_with_filters(
    db: AsyncSession,
    nation: Optional[int] = None,  
    name: Optional[str] = None, 
    team: Optional[int] = None, 
    competition: Optional[int] = None,
    market_value: Optional[float] = None,
    position: Optional[str] = None
) -> List[Player]:
    # Start the base query
    query = select(Player)
    
    # List of dynamic conditions
    conditions = []
    
    # Filter by name (ilike for case-insensitive search)
    if name is not None:
        conditions.append(Player.name.ilike(f"%{name}%"))
    
    # Filter by nationality
    if nation is not None:
        conditions.append(Player.nationality_id == nation)
    
    # Filter by team
    if team is not None:
        conditions.append(Player.team_id == team)
    
    # Filter by competition (this requires a join with TeamCompetition)
    if competition is not None:
        query = query.join(TeamCompetition, Player.team_id == TeamCompetition.team_id)
        conditions.append(TeamCompetition.competition_id == competition)
    
    # Filter by market value
    if market_value is not None:
        conditions.append(Player.market_value < market_value)
    
    # Filter by position (primary or alternate)
    if position is not None:
        conditions.append(or_(
            Player.position == position,
            Player.alternate_position.contains(position)
        ))
    
    # Apply all dynamic conditions
    if conditions:
        query = query.where(and_(*conditions))
    
    try:
        # Execute the query
        result = await db.execute(query)
        players = result.scalars().all()
        return players
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))