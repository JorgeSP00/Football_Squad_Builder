from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.ratings import create_rating, delete_rating, get_rating_by_id, get_rating_for_squad, get_ratings, update_rating
from db import get_db
from models.models import RatingCreate

router=APIRouter()

# Ratings Endpoints
@router.get("/ratings/")
async def read_ratings(db: AsyncSession = Depends(get_db)):
    return {"ratings": await get_ratings(db)}

@router.get("/ratings/{rating_id}")
async def read_rating(rating_id: int, db: AsyncSession = Depends(get_db)):
    return await get_rating_by_id(db, rating_id)

@router.post("/ratings/")
async def create_rating_route(rating: RatingCreate, db: AsyncSession = Depends(get_db)):
    return await create_rating(db, rating)

@router.put("/ratings/{rating_id}")
async def update_rating_route(rating: RatingCreate, rating_id: int, db: AsyncSession = Depends(get_db)):
    return await update_rating(db, rating, rating_id)

@router.delete("/ratings/{rating_id}")
async def delete_rating_route(rating_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_rating(db, rating_id)


@router.get("/ratings_filtered/")
async def read_competition_name(squad_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    if squad_id:
        return await get_rating_for_squad(db, squad_id)
    else:
        raise HTTPException(status_code=400, detail="Please provide a filter parameter: squad_id")