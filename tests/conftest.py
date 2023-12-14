import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from app.main import app

DATABASE_URL = "sqlite:///./test.db"  # Use a separate test database
engine = create_engine(DATABASE_URL)


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def fastapi_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
