import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Dict
from models.models import Usuario, UsuarioCreate


# Obtener todos los usuarios
async def get_users(db: AsyncSession) -> List[Usuario]:
    try:
        result = await db.execute(select(Usuario))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener un usuario por ID
async def get_user_by_id(db: AsyncSession, user_id: int) -> Usuario:
    try:
        result = await db.execute(select(Usuario).where(Usuario.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener un usuario por username
async def get_user_by_username(db: AsyncSession, username: str) -> Usuario:
    try:
        result = await db.execute(select(Usuario).where(Usuario.username == username))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Crear un nuevo usuario (con hasheo de la contraseña)
async def create_user(db: AsyncSession, new_usuario: UsuarioCreate) -> Dict[str, int]:
    try:
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(new_usuario.password.encode('utf-8'), bcrypt.gensalt())
        
        usuario = Usuario(username=new_usuario.username, password=hashed_password.decode('utf-8'), email=new_usuario.email)
        db.add(usuario)
        await db.commit()
        await db.refresh(usuario)
        return usuario
    except SQLAlchemyError as e:
        await db.rollback()  # Reversión en caso de error
        raise HTTPException(status_code=500, detail=str(e))


# Actualizar un usuario existente (con hasheo si cambia la contraseña)
async def update_user(db: AsyncSession, updatedUser: UsuarioCreate, user_id: int) -> None:
    try:
        user = await get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Hashear la nueva contraseña si se proporciona
        hashed_password = bcrypt.hashpw(updatedUser.password.encode('utf-8'), bcrypt.gensalt())
        user.username = updatedUser.username
        user.email = updatedUser.email
        user.password = hashed_password.decode('utf-8')

        await db.commit()
        await db.refresh(user)
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Eliminar un usuario
async def delete_user(db: AsyncSession, user_id: int) -> None:
    try:
        user = await get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        await db.delete(user)
        await db.commit()
        return {"detail": "User with id " + str(user_id) + " deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Verificar credenciales de usuario
async def verify_user_credentials(db: AsyncSession, username: str, password: str) -> int:
    try:
        user = await get_user_by_username(db, username)
        if user is None:
            return None

        # Verificar la contraseña
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user.id
        return False
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))