import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db


@pytest.fixture(scope="session")
def engine():
    # Use in-memory SQLite for tests
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    return test_engine


@pytest.fixture(scope="session", autouse=True)
async def setup_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(engine):
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def override_get_db(db_session):
    async def _get_db():
        return db_session
    return _get_db