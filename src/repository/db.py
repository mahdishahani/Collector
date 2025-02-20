from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config.setup import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)


async def get_async_session() -> AsyncSession:
    async_session_ = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_() as db:
        yield db
