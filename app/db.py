from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from settings.base import settings

DATABASE_URI = (
    f"{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_ENDPOINT}:{settings.DB_PORT}/{settings.DB_NAME}"
)
ASYNC_DATABASE_URI: str = f"postgresql+asyncpg://{DATABASE_URI}"

engine = create_async_engine(ASYNC_DATABASE_URI, poolclass=NullPool, echo=True)

sync_engine = create_engine(f"postgresql://{DATABASE_URI}", echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
