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

## Встановлення

1. Клонуй репозиторій у робочу теку:

```bash
git clone <URL репозиторію> lab3-fastapi
cd lab3-fastapi
```

2. Створи віртуальне оточення (рекомендовано):

```bash
python -m venv venv
```

3. Активуй оточення:

- Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

- Windows CMD:

```cmd
venv\Scripts\activate.bat
```

4. Встанови залежності:

```bash
pip install -r requirements.txt
```

5. Додай `.env` до `.gitignore`, якщо ще не зроблено.

## Локальний запуск

1. Запусти сервер:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Відкрий документацію OpenAPI:

- `http://127.0.0.1:8000/docs`

3. Перевір роботу CRUD-ендпоїнтів:

- `GET /users/`
- `GET /users/{user_id}`
- `POST /users/`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

## Запуск у Docker

1. Побудуй Docker-образ:

```bash
docker build -t lab3-fastapi .
```

2. Запусти контейнер:

```bash
docker run --rm -p 8000:8000 lab3-fastapi
```

3. Або через Docker Compose:

```bash
docker compose up --build
```

## Тестування

1. Встанови `pytest`, якщо ще не встановлено:

```bash
pip install pytest
```

2. Запусти тести:

```bash
python -m pytest -q
```

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

## Примітки

- У цьому проєкті використовується in-memory база даних, тому дані не зберігаються після перезапуску сервера.
- Для повного завершення лабораторної роботи необхідно додати скріншот роботи запитів у гілку `DEV`.
