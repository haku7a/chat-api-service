import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.db.session import async_session_maker


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
