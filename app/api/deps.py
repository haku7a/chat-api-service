from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import async_session_maker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
