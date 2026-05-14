import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings

# Використовуємо тестову базу даних з налаштувань
DATABASE_URL = settings.test_database_url

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def engine():
    # NullPool використовується для тестів, щоб уникнути проблем з паралельними підключеннями
    test_engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield test_engine
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture
async def db_session(engine):
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback() # Відкат змін після кожного тесту

@pytest_asyncio.fixture
async def client(db_session):
    # Підміна залежності get_db на нашу тестову сесію
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    # Скидаємо підміну після тесту
    app.dependency_overrides.clear()