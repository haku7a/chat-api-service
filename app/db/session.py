from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.pool import NullPool
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, poolclass=NullPool)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
