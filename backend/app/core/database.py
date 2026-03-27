from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Support SQLite (dev) and PostgreSQL (prod)
_url = settings.database_url
if _url.startswith("postgresql://"):
    database_url = _url.replace("postgresql://", "postgresql+asyncpg://")
elif _url.startswith("sqlite"):
    database_url = _url  # already in correct format e.g. sqlite+aiosqlite:///./db.sqlite
else:
    database_url = _url

engine = create_async_engine(database_url, echo=settings.debug)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """Dependency that provides a database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Create all tables. Call on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
