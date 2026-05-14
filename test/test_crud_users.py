import pytest
from app.crud import crud_user
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_user_crud(db_session: AsyncSession):
    user_in = UserCreate(username="crud_test", email="crud@test.com", password="password123")
    user = await crud_user.create_user(db_session, user_in)
    assert user.username == "crud_test"
    assert user.id is not None
    assert user.hashed_password != "password123" # Перевірка, що пароль захешовано

@pytest.mark.asyncio
async def test_get_user_crud(db_session: AsyncSession):
    user_in = UserCreate(username="get_test", email="get@test.com", password="password")
    created_user = await crud_user.create_user(db_session, user_in)
    
    fetched_user = await crud_user.get_user(db_session, created_user.id)
    assert fetched_user.id == created_user.id
    assert fetched_user.username == "get_test"

@pytest.mark.asyncio
async def test_list_users_crud(db_session: AsyncSession):
    # Очистка або перевірка кількості може залежати від стану БД, 
    # але оскільки фікстура db_session робить rollback, тут має бути чисто.
    user1 = UserCreate(username="u1", email="u1@t.com", password="p")
    user2 = UserCreate(username="u2", email="u2@t.com", password="p")
    await crud_user.create_user(db_session, user1)
    await crud_user.create_user(db_session, user2)
    
    users = await crud_user.list_users(db_session)
    assert len(users) >= 2
