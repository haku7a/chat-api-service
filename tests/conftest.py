import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.db.session import async_session_maker, engine
from sqlmodel import SQLModel


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
