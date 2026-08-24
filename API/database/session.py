from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

from config import db_settings

# Create async engine
engine: AsyncEngine = create_async_engine(url=db_settings.connection_url)


async def create_database_and_tables() -> None:
    print("-------------------------------- Entering create_database_and_tables")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    print("-------------------------------- Entering get_session")
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
