from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/login")
async def login(
    response: Response,
    payload: UserCreate, # Використовуємо UserCreate для простоти (username + password)
    db: AsyncSession = Depends(get_db)
):
    # Шукаємо користувача
    result = await db.execute(select(User).where(User.username == payload.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
        )

    # Створюємо токен
    access_token = create_access_token(data={"sub": user.username})
    
    # Встановлюємо кукі (HttpOnly для безпеки)
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True, 
        max_age=1800, # 30 хвилин
        samesite="lax"
    )
    
    return {"message": "Вхід успішний", "username": user.username}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вихід успішний"}
