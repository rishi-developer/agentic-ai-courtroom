from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from app.config.settings import settings
from app.database.base import Base

DATABASE_URL = "sqlite+aiosqlite:///./courtroom.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    import app.models
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)