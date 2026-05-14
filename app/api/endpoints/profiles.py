from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import crud_profile
from app.models.profile import UserProfile
from pydantic import BaseModel

router = APIRouter()

class ProfileRead(BaseModel):
    id: int
    full_name: str
    bio: str
    user_id: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ProfileRead)
async def create_profile(payload: crud_profile.ProfileCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already has a profile
    existing = await crud_profile.get_profile_by_user_id(db, payload.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")
    return await crud_profile.create_profile(db, payload)

@router.get("/{profile_id}", response_model=ProfileRead)
async def read_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await crud_profile.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/user/{user_id}", response_model=ProfileRead)
async def read_profile_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    profile = await crud_profile.get_profile_by_user_id(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(profile_id: int, payload: crud_profile.ProfileUpdate, db: AsyncSession = Depends(get_db)):
    profile = await crud_profile.update_profile(db, profile_id, payload)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.delete("/{profile_id}")
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud_profile.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted"}
