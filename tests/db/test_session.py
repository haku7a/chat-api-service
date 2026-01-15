import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession


async def test_database_connection(db_session: AsyncSession):
    result = await db_session.exec(text("SELECT 1"))
    assert result.scalar() == 1
