from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def list_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    # Перетворюємо EmailStr у звичайний рядок для бази даних
    db_user = User(
        username=payload.username,
        email=str(payload.email),
        hashed_password=payload.password,  # В реальних проектах тут має бути хешування
        is_active=payload.is_active,
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        await db.rollback()
        raise e
    return db_user


async def update_user(db: AsyncSession, user_id: int, payload: UserUpdate) -> User | None:
    user = await get_user(db, user_id)
    if not user:
        return None

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        if key == "email":
            setattr(user, key, str(value))
        else:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True