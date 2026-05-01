from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import UserProfile
from pydantic import BaseModel


class ProfileCreate(BaseModel):
    full_name: str
    bio: str
    user_id: int


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None


async def get_profile(db: AsyncSession, profile_id: int) -> UserProfile | None:
    result = await db.execute(select(UserProfile).where(UserProfile.id == profile_id))
    return result.scalar_one_or_none()


async def get_profile_by_user_id(db: AsyncSession, user_id: int) -> UserProfile | None:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    return result.scalar_one_or_none()


async def create_profile(db: AsyncSession, payload: ProfileCreate) -> UserProfile:
    profile = UserProfile(**payload.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def update_profile(db: AsyncSession, profile_id: int, payload: ProfileUpdate) -> UserProfile | None:
    profile = await get_profile(db, profile_id)
    if not profile:
        return None
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(profile, key, value)
    
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_profile(db: AsyncSession, profile_id: int) -> bool:
    profile = await get_profile(db, profile_id)
    if not profile:
        return False
    
    await db.delete(profile)
    await db.commit()
    return True
