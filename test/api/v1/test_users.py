import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db.session import get_db


@pytest.fixture
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "secret",
            "is_active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "test_user"
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True


def test_read_users_and_user_by_id(client):
    client.post(
        "/users/",
        json={
            "username": "reader",
            "email": "reader@example.com",
            "password": "secret",
            "is_active": True,
        },
    )

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]["username"] == "reader"

    get_response = client.get("/users/1")
    assert get_response.status_code == 200
    user = get_response.json()
    assert user["email"] == "reader@example.com"


def test_update_user(client):
    client.post(
        "/users/",
        json={
            "username": "updatable",
            "email": "update@example.com",
            "password": "secret",
            "is_active": True,
        },
    )

    update_response = client.put(
        "/users/1",
        json={
            "username": "updated",
            "email": "updated@example.com",
            "is_active": False,
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["username"] == "updated"
    assert updated["email"] == "updated@example.com"
    assert updated["is_active"] is False


def test_delete_user(client):
    client.post(
        "/users/",
        json={
            "username": "deletable",
            "email": "delete@example.com",
            "password": "secret",
            "is_active": True,
        },
    )

    delete_response = client.delete("/users/1")
    assert delete_response.status_code == 204

    missing_response = client.get("/users/1")
    assert missing_response.status_code == 404
