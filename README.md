# Lab 4 — FastAPI PostgreSQL CRUD

Лабораторна робота з FastAPI: реалізовано CRUD для користувачів, постів, категорій, коментарів та тегів з використанням PostgreSQL СУБД та асинхронної роботи з БД.

## Опис

- Використано FastAPI з асинхронною роботою
- PostgreSQL як СУБД
- SQLAlchemy з asyncpg для асинхронних запитів
- Alembic для міграцій БД
- Pydantic для конфігурації та валідації
- Моделі з relationships: one-to-many, one-to-one, many-to-many
- CRUD для всіх моделей
- Seed data для тестування

## Структура проєкту

- `app/main.py` — запуск FastAPI-додатку з автостворенням таблиць
- `app/api/router.py` — підключення всіх роутерів
- `app/api/endpoints/` — CRUD-ендпоїнти для всіх моделей
- `app/schemas/` — Pydantic-схеми для всіх моделей
- `app/crud/` — логіка CRUD для всіх моделей
- `app/models/` — SQLAlchemy моделі з relationships
- `app/db/session.py` — async session factory
- `app/db/base.py` — базова декларативна база
- `app/core/config.py` — Pydantic конфігурація
- `alembic/` — міграції БД
- `seed_data.py` — скрипт для додавання тестових даних

## Моделі та Relationships

- **User**: базова модель користувача
- **Category**: категорії постів (one-to-many з Post)
- **Post**: пости (many-to-one з User та Category, one-to-many з Comment, many-to-many з Tag)
- **Comment**: коментарі (many-to-one з User та Post)
- **Tag**: теги (many-to-many з Post через PostTag)

## Встановлення

1. Клонуй репозиторій:

```bash
git clone <URL репозиторію> lab4-fastapi-postgres
cd lab4-fastapi-postgres
```

2. Встанови Poetry (якщо ще не встановлено):
   [Інструкція з встановлення Poetry](https://python-poetry.org/docs/#installation)

3. Встанови залежності:

```bash
poetry install
```

4. Активуй віртуальне оточення:

```bash
poetry shell
```

4. Налаштуй змінні середовища в `.env` (якщо потрібно).

## Запуск з Docker Compose

1. Запусти сервіси:

```bash
docker compose up --build
```

2. Застосуй міграції (в окремому терміналі):

```bash
docker compose exec api alembic upgrade head
```

3. Додай тестові дані:

```bash
docker compose exec api python seed_data.py
```

## Локальний запуск

1. Запусти PostgreSQL (локально або через Docker):

```bash
docker run --name postgres -e POSTGRES_PASSWORD=changeme -e POSTGRES_DB=lab4_db -p 5432:5432 -d postgres:16
```

2. Застосуй міграції:

```bash
poetry run alembic upgrade head
```

3. Додай тестові дані:

```bash
poetry run python seed_data.py
```

4. Запусти сервер:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Відкрий документацію:

- `http://127.0.0.1:8000/docs`

## API Ендпоїнти

### Users
- `GET /users/` — список користувачів
- `GET /users/{id}` — користувач за ID
- `POST /users/` — створити користувача
- `PUT /users/{id}` — оновити користувача
- `DELETE /users/{id}` — видалити користувача

### Posts
- `GET /posts/` — список постів
- `GET /posts/{id}` — пост за ID
- `POST /posts/` — створити пост
- `PUT /posts/{id}` — оновити пост
- `DELETE /posts/{id}` — видалити пост

### Categories
- `GET /categories/` — список категорій
- `GET /categories/{id}` — категорія за ID
- `POST /categories/` — створити категорію
- `PUT /categories/{id}` — оновити категорію
- `DELETE /categories/{id}` — видалити категорію

### Comments
- `GET /comments/` — список коментарів
- `GET /comments/{id}` — коментар за ID
- `POST /comments/` — створити коментар
- `PUT /comments/{id}` — оновити коментар
- `DELETE /comments/{id}` — видалити коментар

### Tags
- `GET /tags/` — список тегів
- `GET /tags/{id}` — тег за ID
- `POST /tags/` — створити тег
- `PUT /tags/{id}` — оновити тег
- `DELETE /tags/{id}` — видалити тег

## Міграції

Створити нову міграцію:

```bash
alembic revision --autogenerate -m "Your message"
```

Застосувати міграції:

```bash
alembic upgrade head
```

## Тестування

```bash
poetry run pytest -q
```

## Seed Data

Скрипт `seed_data.py` додає:

- 2 користувачів
- 2 категорії
- 2 пости
- 2 коментарі
- 3 теги

## Примітки

- Усі запити до БД асинхронні
- Використано SQLAlchemy 2.0 з async/await
- Alembic керує міграціями
- Pydantic для конфігурації та схем
- Для повного завершення лабораторної роботи додати скріншоти БД з даними у гілку `DEV`
