from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

# Pydantic моделі
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int

# Тестовий endpoint
@router.get("/")
async def read_users():
    return [{"id": 1, "name": "Bohdan", "email": "bohdan@example.com"}]