from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.app.core.db.config import db_settings


class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    str(db_settings.DATABASE_URL),
    echo=db_settings.DB_ECHO,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
