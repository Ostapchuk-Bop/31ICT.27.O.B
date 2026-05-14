from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Отримати інформацію про поточного авторизованого користувача.
    Вимагає наявності валідного JWT у куках.
    """
    return current_user

@router.get("/", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud_user.list_users(db)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # Перевірка, чи існує вже користувач з таким ніком або поштою
    from sqlalchemy import or_, select
    from app.models.user import User
    
    existing_user = await db.execute(
        select(User).where(
            or_(User.username == payload.username, User.email == str(payload.email))
        )
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists",
        )
    
    return await crud_user.create_user(db, payload)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return None
