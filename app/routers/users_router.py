from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from crud.usuarios import create_user, delete_user, get_user_by_id, get_users, update_user, verify_user_credentials
from models.models import UserCredentials, UsuarioCreate

router=APIRouter()

# Users Endpoints
@router.get("/users/")
async def read_users(db: AsyncSession = Depends(get_db)):
    return {"users": await get_users(db)}

@router.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@router.post("/users/")
async def create_user_route(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, usuario)

@router.put("/users/{user_id}")
async def update_user_route(usuario: UsuarioCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    return await update_user(db, usuario, user_id)

@router.delete("/users/{user_id}")
async def delete_user_route(user_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_user(db, user_id)

@router.post("/users/verify/")
async def verify_user_route(credentials: UserCredentials, db: AsyncSession = Depends(get_db)):
    is_valid = await verify_user_credentials(db, credentials.username, credentials.password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return is_valid