from typing import List

from fastapi import APIRouter
from app.crud import crud_user_mem
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def read_users():
    return crud_user_mem.list_users()

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    return crud_user_mem.get_user(user_id)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate):
    return crud_user_mem.create_user(payload)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate):
    return crud_user_mem.update_user(user_id, payload)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    crud_user_mem.delete_user(user_id)
    return None
