import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_api(client: AsyncClient):
    response = await client.post(
        "/users/",
        json={"username": "api_test", "email": "api@test.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "api_test"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_users_api(client: AsyncClient):
    # Створимо користувача спочатку
    await client.post(
        "/users/",
        json={"username": "list_test", "email": "list@test.com", "password": "password"}
    )
    
    response = await client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

@pytest.mark.asyncio
async def test_login_and_me_api(client: AsyncClient):
    # 1. Реєструємося
    await client.post(
        "/users/",
        json={"username": "auth_test", "email": "auth@test.com", "password": "password123"}
    )
    
    # 2. Логінимося
    login_res = await client.post(
        "/auth/login",
        json={"username": "auth_test", "email": "auth@test.com", "password": "password123"}
    )
    assert login_res.status_code == 200
    assert "access_token" in client.cookies
    
    # 3. Перевіряємо доступ до /users/me
    me_res = await client.get("/users/me")
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "auth_test"

@pytest.mark.asyncio
async def test_logout_api(client: AsyncClient):
    # Логінимося
    await client.post(
        "/users/",
        json={"username": "logout_test", "email": "logout@test.com", "password": "p"}
    )
    await client.post(
        "/auth/login",
        json={"username": "logout_test", "email": "logout@test.com", "password": "p"}
    )
    assert "access_token" in client.cookies
    
    # Виходимо
    logout_res = await client.post("/auth/logout")
    assert logout_res.status_code == 200
    assert "access_token" not in client.cookies
