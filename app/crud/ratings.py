from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from models.models import Rating, RatingCreate

# Get all ratings
async def get_ratings(db: AsyncSession) -> List[Rating]:
    try:
        result = await db.execute(select(Rating))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a rating by ID
async def get_rating_by_id(db: AsyncSession, rating_id: int) -> Rating:
    try:
        result = await db.execute(select(Rating).where(Rating.id == rating_id))
        rating = result.scalar_one_or_none()
        if rating is None:
            raise HTTPException(status_code=404, detail="Not found rating")
        return rating
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new rating
async def create_rating(db: AsyncSession, new_rating: RatingCreate) -> Dict[str, int]:
    try:
        rating = Rating(
            rating=new_rating.rating, 
            comment=new_rating.comment, 
            squad_id=new_rating.squad_id, 
            user_id=new_rating.user_id
        )
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        return rating
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update an existing rating
async def update_rating(db: AsyncSession, updated_rating: RatingCreate, rating_id: int) -> None:
    try:
        rating = await get_rating_by_id(db, rating_id)
        if rating is None:
            raise HTTPException(status_code=404, detail="Not found rating")

        rating.rating = updated_rating.rating
        rating.comment = updated_rating.comment
        rating.squad_id = updated_rating.squad_id
        rating.user_id = updated_rating.user_id

        await db.commit()

        await db.refresh(rating)
        return rating
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not update rating: " + str(e))

# Delete a rating
async def delete_rating(db: AsyncSession, rating_id: int) -> None:
    try:
        result = await get_rating_by_id(db, rating_id)
        rating = result.scalar_one_or_none()
        if rating is None:
            raise HTTPException(status_code=404, detail="Not found rating")

        await db.delete(rating)
        await db.commit()
        return {"detail": "Rating with id " + str(rating_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Other gets
# Get ratings for a squad
async def get_rating_for_squad(db: AsyncSession, squad_id: int) -> Rating:
    try:
        result = await db.execute(select(Rating).where(Rating.squad_id == squad_id))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))