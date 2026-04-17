# Lab 3 — FastAPI CRUD for Users

Лабораторна робота з FastAPI: реалізовано CRUD для користувачів з тимчасовою емуляцією бази даних через простий словник.

## Опис

- Використано FastAPI
- Емуляція бази даних через `app/db/mem_db.py`
- Використано роутери: `app/api/router.py` та `app/api/endpoints/users.py`
- Валідація даних через Pydantic-схеми: `app/schemas/user.py`
- Точка входу: `app/main.py`
- Docker-стартап через `entrypoint.sh`

## Структура проєкту

- `app/main.py` — запуск FastAPI-додатку
- `app/api/router.py` — підключення роутерів
- `app/api/endpoints/users.py` — CRUD-ендпоїнти для користувачів
- `app/schemas/user.py` — Pydantic-схеми
- `app/crud/crud_user_mem.py` — логіка CRUD над in-memory словником
- `app/db/mem_db.py` — in-memory база даних
- `Dockerfile` — контейнеризація через точку входу
- `entrypoint.sh` — скрипт запуску сервера

## Запити

Підтримуються наступні HTTP-методи:

- `GET /users/` — отримати список користувачів
- `GET /users/{user_id}` — отримати користувача за ID
- `POST /users/` — створити користувача
- `PUT /users/{user_id}` — оновити користувача
- `DELETE /users/{user_id}` — видалити користувача

## Формат даних

### Запит для створення користувача

```json
{
  "username": "oleg",
  "email": "oleg@example.com",
  "password": "secret",
  "is_active": true
}
```

### Запит для оновлення користувача

```json
{
  "username": "oleg_updated",
  "email": "oleg2@example.com",
  "is_active": false
}
```

## Запуск локально

1. Встановити залежності:

```bash
pip install -r requirements.txt
```

2. Запустити сервер:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Відкрити Swagger UI:

- `http://127.0.0.1:8000/docs`

## Запуск у Docker

1. Побудувати образ:

```bash
docker build -t lab3-fastapi .
```

2. Запустити контейнер:

```bash
docker run --rm -p 8000:8000 lab3-fastapi
```

Або через Docker Compose (якщо потрібно):

```bash
docker compose up --build
```

## Примітки

- У цьому проєкті використовується in-memory база даних, тому дані не зберігаються після перезапуску сервера.
- Для повного завершення лабораторної роботи необхідно додати скріншот роботи запитів у гілку `DEV`.
